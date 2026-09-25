import http from 'node:http';
import {readFile,stat,writeFile,mkdir} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const port=Number(process.env.PORT||4173);
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png','.glb':'model/gltf-binary','.mp4':'video/mp4'};
http.createServer(async(req,res)=>{
  try{
    const url=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    if(req.method==='POST'&&url==='/record'){
      const origin=req.headers.origin;
      if(origin!==`http://127.0.0.1:${port}`){res.writeHead(403);return res.end('Forbidden origin');}
      const chunks=[];let size=0;
      for await(const chunk of req){
        size+=chunk.length;
        if(size>100_000_000)throw Error('Recording exceeds 100 MB');
        chunks.push(chunk);
      }
      if(!size)throw Error('Recording is empty');
      const renders=path.resolve(root,'../renders');
      await mkdir(renders,{recursive:true});
      await writeFile(path.join(renders,'holo-motion.webm'),Buffer.concat(chunks));
      res.writeHead(200,{'Content-Type':'text/plain; charset=utf-8'});
      return res.end('saved');
    }
    if(req.method!=='GET'){res.writeHead(405);return res.end('Method not allowed');}
    let filename=path.resolve(root,'.'+url);
    if(filename!==root&&!filename.startsWith(root+path.sep)){res.writeHead(403);return res.end('Forbidden');}
    if((await stat(filename)).isDirectory())filename=path.join(filename,'index.html');
    const data=await readFile(filename);
    res.writeHead(200,{'Content-Type':types[path.extname(filename)]||'application/octet-stream','Cache-Control':'no-cache'});
    res.end(data);
  }catch(error){res.writeHead(404);res.end(error.message||'Not found');}
}).listen(port,'127.0.0.1',()=>console.log(`Holo Card Studio: http://127.0.0.1:${port}`));
