const frame=document.querySelector('#card');
const start=document.querySelector('#start');
const status=document.querySelector('#status');
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));

frame.addEventListener('load',()=>{
  const timer=setInterval(()=>{
    if(frame.contentWindow.__holo?.ready){
      clearInterval(timer);
      start.disabled=false;
      status.textContent='准备就绪';
    }else if(frame.contentWindow.__holo?.error){
      clearInterval(timer);
      status.textContent='卡片加载失败：'+frame.contentWindow.__holo.error;
    }
  },200);
});

start.addEventListener('click',async()=>{
  start.disabled=true;
  let recorder,stream;
  try{
    const win=frame.contentWindow,doc=win.document;
    if(!win.__holo?.ready)throw Error('卡片仍在加载');
    const display=doc.querySelector('.display');
    display.style.width='720px';
    display.style.height='1080px';
    display.style.minHeight='1080px';
    display.style.maxHeight='none';
    await delay(500);
    const canvas=win.__holo.renderer.domElement;
    if(typeof canvas.captureStream!=='function'||typeof MediaRecorder==='undefined')throw Error('当前浏览器不支持画布录制');
    const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(type=>MediaRecorder.isTypeSupported(type));
    if(!mime)throw Error('当前浏览器不支持 WebM 录制');
    doc.querySelector('#reset').click();
    stream=canvas.captureStream(30);
    const chunks=[];
    recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:6_000_000});
    recorder.addEventListener('dataavailable',event=>{if(event.data.size)chunks.push(event.data);});
    recorder.addEventListener('stop',async()=>{
      try{
        status.textContent='正在保存…';
        const blob=new Blob(chunks,{type:mime});
        const response=await fetch('/record',{method:'POST',body:blob});
        if(!response.ok)throw Error(await response.text());
        status.textContent=`已保存 WebM（${(blob.size/1024/1024).toFixed(1)} MB）；下一步运行 scripts/export_video.py`;
      }catch(error){status.textContent='保存失败：'+error.message;}
      stream.getTracks().forEach(track=>track.stop());
      start.disabled=false;
    });
    recorder.start();
    status.textContent='录制中：正面流光';
    doc.querySelector('#auto').click();
    await delay(2600);
    status.textContent='录制中：翻至背面';
    doc.querySelector('#flip').click();
    await delay(2300);
    status.textContent='录制中：返回正面';
    doc.querySelector('#flip').click();
    await delay(700);
    doc.querySelector('#auto').click();
    await delay(1700);
    recorder.stop();
  }catch(error){
    if(recorder?.state==='recording')recorder.stop();
    if(stream)stream.getTracks().forEach(track=>track.stop());
    status.textContent='录制失败：'+error.message;
    start.disabled=false;
  }
});
