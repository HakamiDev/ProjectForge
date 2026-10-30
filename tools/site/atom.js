<script>/*ATOM*/(function(){
if(window.ForgeAtom)return;
var TAU=Math.PI*2,RED=false;try{RED=matchMedia("(prefers-reduced-motion:reduce)").matches}catch(e){}
function mul(a,b){var r=[0,0,0,0,0,0,0,0,0],i,j,k;for(i=0;i<3;i++)for(j=0;j<3;j++){var s=0;for(k=0;k<3;k++)s+=a[i*3+k]*b[k*3+j];r[i*3+j]=s}return r}
function rot(ax,ay,az,ang){var l=Math.sqrt(ax*ax+ay*ay+az*az)||1;ax/=l;ay/=l;az/=l;var c=Math.cos(ang),s=Math.sin(ang),t=1-c;
return[t*ax*ax+c,t*ax*ay-s*az,t*ax*az+s*ay,t*ax*ay+s*az,t*ay*ay+c,t*ay*az-s*ax,t*ax*az-s*ay,t*ay*az+s*ax,t*az*az+c]}
function ortho(m){/* يمنع تراكم الخطأ العددي */var a=[m[0],m[1],m[2]],b=[m[3],m[4],m[5]],l=Math.hypot(a[0],a[1],a[2]);a=a.map(function(v){return v/l});
var d=a[0]*b[0]+a[1]*b[1]+a[2]*b[2];b=[b[0]-d*a[0],b[1]-d*a[1],b[2]-d*a[2]];l=Math.hypot(b[0],b[1],b[2]);b=b.map(function(v){return v/l});
var c=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];return[a[0],a[1],a[2],b[0],b[1],b[2],c[0],c[1],c[2]]}
/* نفس شعار الموقع الأول: بلاطة متدرّجة (نعناعي ← سماوي ← بنفسجي) وعليها نواة بيضاء وثلاث عقد (أعلى، يسار أسفل، يمين أسفل) تربطها سيقان؛ هنا مجسّم حقيقي يدور في الفضاء وتبدأ زاويته من وضع الشعار نفسه */
var C=[0,0,0],NO=[[0,-.5625,0],[-.484,.281,0],[.484,.281,0]],RC=.1875,RN=.117,RS=.055,all=[];
function mount(el){
 if(!el||el.__atom)return;el.__atom=1;
 var sz=Math.max(24,Math.round(el.getBoundingClientRect().width||el.offsetWidth||34)),dpr=Math.min(window.devicePixelRatio||1,3);
 var cv=document.createElement("canvas");cv.width=cv.height=Math.round(sz*dpr);cv.style.cssText="width:100%;height:100%;display:block;pointer-events:none;border-radius:24%";cv.setAttribute("aria-hidden","true");
 el.style.background="none";el.style.webkitMaskImage="none";el.style.maskImage="none";el.style.boxShadow="none";el.style.animation="none";el.style.filter="none";el.style.transform="none";
 Array.prototype.forEach.call(el.children,function(c){c.style.display="none"});
 el.appendChild(cv);
 var st={x:cv.getContext("2d"),s:cv.width,R:[1,0,0,0,1,0,0,0,1],w:[.5,.8,.3],t:0,seed:[Math.random()*9,Math.random()*9,Math.random()*9]};
 all.push(st);draw(st);start();
 if(window.ResizeObserver){new ResizeObserver(function(){var w=Math.round(el.getBoundingClientRect().width*dpr);if(w>8&&w!==cv.width){cv.width=cv.height=w;st.s=w;draw(st)}}).observe(el)}
}
function tile(x,S){var r=S*60/256,g=x.createLinearGradient(0,0,S,S);g.addColorStop(0,"#4087F1");g.addColorStop(.5,"#1F5CB8");g.addColorStop(1,"#0B0C0E");
 x.fillStyle=g;x.beginPath();x.moveTo(r,0);x.arcTo(S,0,S,S,r);x.arcTo(S,S,0,S,r);x.arcTo(0,S,0,0,r);x.arcTo(0,0,S,0,r);x.closePath();x.fill()}
/* المقاسات من logo.svg حرفيًا (وحدة 256): النواة نصف قطرها 24، والعقد 15، والساق سمكها 14؛ المراكز (128,128) و(128,56) و(66,164) و(190,164). الألوان ثابتة كما هي: أبيض صافٍ على البلاطة المتدرّجة. */
function draw(a){
 var x=a.x,S=a.s,R=a.R,cx=S/2,sc=S/2,D=6,items=[];
 function T(v){return[R[0]*v[0]+R[1]*v[1]+R[2]*v[2],R[3]*v[0]+R[4]*v[1]+R[5]*v[2],R[6]*v[0]+R[7]*v[1]+R[8]*v[2]]}
 function P(V){var f=D/(D-V[2]);return[cx+V[0]*f*sc,cx+V[1]*f*sc,V[2],f]}
 x.clearRect(0,0,S,S);tile(x,S);
 var c3=T(C),c0=P(c3);items.push({z:c3[2],k:"s",p:c0,r:RC});
 NO.forEach(function(n){var n3=T(n),d=[n3[0]-c3[0],n3[1]-c3[1],n3[2]-c3[2]],L=Math.hypot(d[0],d[1],d[2]);d=[d[0]/L,d[1]/L,d[2]/L];
  /* الساق تبدأ من سطح النواة وتنتهي عند سطح العقدة، فنقطة الالتصاق تظهر حين تتجه الساق نحو الناظر وتختفي خلف الكرة حين تبتعد */
  var s0=Math.sqrt(Math.max(0,RC*RC-RS*RS)),s1=L-Math.sqrt(Math.max(0,RN*RN-RS*RS)),A=[c3[0]+d[0]*s0,c3[1]+d[1]*s0,c3[2]+d[2]*s0],B=[c3[0]+d[0]*s1,c3[1]+d[1]*s1,c3[2]+d[2]*s1];
  items.push({z:n3[2],k:"s",p:P(n3),r:RN});
  items.push({z:(A[2]+B[2])/2,k:"b",a:P(A),b:P(B),dz:d[2]});
 });
 /* ترتيب الرسم من الأبعد إلى الأقرب */
 items.sort(function(m,n){return m.z-n.z});
 x.fillStyle=x.strokeStyle="#ffffff";x.lineCap="butt";
 for(var i=0;i<items.length;i++){var it=items[i];
  if(it.k==="b"){var f=(it.a[3]+it.b[3])/2;x.lineWidth=2*RS*sc*f;x.beginPath();x.moveTo(it.a[0],it.a[1]);x.lineTo(it.b[0],it.b[1]);x.stroke()}
  else{x.beginPath();x.arc(it.p[0],it.p[1],it.r*sc*it.p[3],0,TAU);x.fill()}
 }
}
var raf=0,prevT=0,inkT=0;
function tick(t){
 raf=requestAnimationFrame(tick);
 var dt=Math.min(.05,(t-prevT)/1000);if(t-prevT<30)return;prevT=t;
 
 all.forEach(function(a){
  a.t+=dt;var s=a.seed,w=a.w;
  /* سرعة زاويّة تتغيّر عشوائيًا وبنعومة: دوران متوسط (نحو 1.1 راديان/ث) في اتجاه متقلّب كأنه في الفضاء */
  w[0]=Math.sin(a.t*.37+s[0])*.8+Math.sin(a.t*.91+s[1])*.5;w[1]=Math.sin(a.t*.43+s[1])*.8+Math.sin(a.t*1.07+s[2])*.5;w[2]=Math.sin(a.t*.29+s[2])*.8+Math.sin(a.t*.83+s[0])*.5;
  var m=Math.hypot(w[0],w[1],w[2])||1,sp=1.1;
  a.R=ortho(mul(rot(w[0],w[1],w[2],sp*dt),a.R));
  draw(a);
 });
}
function start(){if(RED||raf)return;raf=requestAnimationFrame(tick)}
document.addEventListener("visibilitychange",function(){if(document.hidden){cancelAnimationFrame(raf);raf=0}else start()});
window.ForgeAtom={mount:mount};
function init(){Array.prototype.forEach.call(document.querySelectorAll(".logo"),mount)}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
/*ENDATOM*/</script>