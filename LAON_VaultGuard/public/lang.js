// lang.js — LAON VaultGuard i18n (KO/EN/ZH/JA)
const LANG={ko:{title:'LAON VaultGuard',scanNow:'Scan Now',scanning:'Scanning...',scanLogs:'Scan Logs',alertSettings:'Alert Settings',report:'Report',setupAlerts:'Setup Alerts',github:'GitHub',refresh:'Refresh',allRepos:'All repos',all:'All',severity:'Severity',repo:'Repo',type:'Type',file:'File',detectedAt:'Detected',action:'Action',confirm:'Confirm',undo:'Undo',note:'Note',close:'Close',openFindings:'Open',totalScans:'Scans',registeredRepos:'Repos',lastScan:'Last Scan',loading:'Loading...',noFindings:'No issues detected',done:'Done'},en:{title:'LAON VaultGuard',scanNow:'Scan Now',scanning:'Scanning...',scanLogs:'Scan Logs',alertSettings:'Alert Settings',report:'Report',setupAlerts:'Setup Alerts',github:'GitHub',refresh:'Refresh',allRepos:'All repos',all:'All',severity:'Severity',repo:'Repo',type:'Type',file:'File',detectedAt:'Detected',action:'Action',confirm:'Confirm',undo:'Undo',note:'Note',close:'Close',openFindings:'Open',totalScans:'Scans',registeredRepos:'Repos',lastScan:'Last Scan',loading:'Loading...',noFindings:'No issues detected',done:'Done'},zh:{title:'LAON VaultGuard',scanNow:'Scan Now',scanning:'Scanning...',scanLogs:'Scan Logs',alertSettings:'Alerts',report:'Report',setupAlerts:'Setup',github:'GitHub',refresh:'Refresh',allRepos:'All',all:'All',severity:'Severity',repo:'Repo',type:'Type',file:'File',detectedAt:'Time',action:'Action',confirm:'Confirm',undo:'Undo',note:'Note',close:'Close',openFindings:'Open',totalScans:'Scans',registeredRepos:'Repos',lastScan:'Last',loading:'...',noFindings:'No issues',done:'Done'},ja:{title:'LAON VaultGuard',scanNow:'Scan',scanning:'Scan...',scanLogs:'Logs',alertSettings:'Alerts',report:'Report',setupAlerts:'Setup',github:'GitHub',refresh:'Refresh',allRepos:'All',all:'All',severity:'Severity',repo:'Repo',type:'Type',file:'File',detectedAt:'Time',action:'Action',confirm:'Confirm',undo:'Undo',note:'Memo',close:'Close',openFindings:'Open',totalScans:'Scans',registeredRepos:'Repos',lastScan:'Last',loading:'...',noFindings:'None',done:'Done'}};

function browserLang(){var l=(navigator.language||'en').slice(0,2);return['ko','ja','zh'].includes(l)?l:'en';}
var currentLang=localStorage.getItem('laon-lang')||browserLang();

function t(key){return(LANG[currentLang]&&LANG[currentLang][key])||LANG['en'][key]||key;}

function setLang(lang){
  currentLang=lang;
  localStorage.setItem('laon-lang',lang);
  applyTranslations();
  if(typeof loadFindings==='function'){loadFindings();loadStatus();}
}

function applyTranslations(){
  document.querySelectorAll('[data-t]').forEach(function(el){
    var key=el.getAttribute('data-t');
    if(el.tagName==='OPTION'){el.textContent=t(key);el.value=t(key);}
    else el.textContent=t(key);
  });
  // update select value to match
  var sel=document.querySelector('select[onchange*="setLang"]');
  if(sel)sel.value=currentLang;
}

// apply on DOM ready
document.addEventListener('DOMContentLoaded',function(){
  applyTranslations();
  var sel=document.querySelector('select[onchange*="setLang"]');
  if(sel)sel.value=currentLang;
});
