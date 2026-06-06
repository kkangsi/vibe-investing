/**
 * 데이터 캐시 레이어 (R2) — "가져온 데이터를 스토리지에 넣고 꺼내 쓴다".
 *
 * 목적(가용성): 외부 소스(Yahoo/FRED)가 한 번 삐끗해도 마지막으로 저장한 시계열로 계속 동작.
 *  - fetch 성공 → R2 에 갱신 저장
 *  - fetch 실패 → R2 의 직전 저장본으로 폴백(stale)
 *  - 둘 다 없음 → 누락(엔진이 결측 처리: ARDS 프록시 폴백 등)
 *
 * (Stooq 처럼 Worker 가 직접 못 받는 소스를 외부 로더로 적재해 두는 용도로도 동일 키 규약 사용 가능.)
 */
import type { DSeries } from "../../shared/strategy/ards/dseries";

/** R2Bucket 의 최소 표면(테스트에서 fake 로 대체). R2Bucket 이 구조적으로 만족. */
export interface R2Like {
  get(key: string): Promise<{ text(): Promise<string> } | null>;
  put(key: string, value: string, options?: unknown): Promise<unknown>;
}

function keyFor(kind: string, id: string): string {
  return `cache/${kind}/${encodeURIComponent(id)}.json`;
}

export async function putSeries(bucket: R2Like, kind: string, id: string, ds: DSeries): Promise<void> {
  await bucket.put(keyFor(kind, id), JSON.stringify(ds), {
    httpMetadata: { contentType: "application/json" },
  });
}

export async function getSeries(bucket: R2Like, kind: string, id: string): Promise<DSeries | null> {
  const obj = await bucket.get(keyFor(kind, id));
  if (!obj) return null;
  try {
    const ds = JSON.parse(await obj.text()) as DSeries;
    return ds && Array.isArray(ds.values) && ds.values.length > 0 ? ds : null;
  } catch {
    return null;
  }
}

export interface ReconcileResult {
  data: Record<string, DSeries>;
  fromCache: string[]; // 폴백으로 캐시에서 가져온 id
  missing: string[]; // fetch·캐시 모두 없음
}

/**
 * fetch 결과를 캐시와 합친다: 성공분은 캐시 갱신 + 사용, 실패분은 캐시 폴백.
 * @param fetched fetchDailyMany/fetchFredMany 의 data (성공분만)
 */
export async function reconcileWithCache(
  bucket: R2Like,
  kind: string,
  ids: string[],
  fetched: Record<string, DSeries>,
): Promise<ReconcileResult> {
  const data: Record<string, DSeries> = {};
  const fromCache: string[] = [];
  const missing: string[] = [];
  for (const id of ids) {
    if (fetched[id]) {
      data[id] = fetched[id];
      await putSeries(bucket, kind, id, fetched[id]); // 캐시 갱신
    } else {
      const cached = await getSeries(bucket, kind, id);
      if (cached) {
        data[id] = cached;
        fromCache.push(id);
      } else {
        missing.push(id);
      }
    }
  }
  return { data, fromCache, missing };
}
