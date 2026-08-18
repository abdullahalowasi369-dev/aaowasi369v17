import { createServer } from "node:http";
import fs from "node:fs";
import path from "node:path";
const base=fs.existsSync("out/index.html")?"out":".";
const mime={".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"text/javascript; charset=utf-8",".txt":"text/plain; charset=utf-8",".xml":"application/xml; charset=utf-8",".docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document",".xlsx":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",".pptx":"application/vnd.openxmlformats-officedocument.presentationml.presentation",".pdf":"application/pdf"};
createServer((req,res)=>{let url=decodeURI((req.url||"/").split("?")[0]);let file=path.join(base,url==="/"?"index.html":url);if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,"index.html");if(!fs.existsSync(file))file=path.join(base,"404.html");res.setHeader("Content-Type",mime[path.extname(file)]||"application/octet-stream");fs.createReadStream(file).pipe(res);}).listen(4173,()=>console.log("Serving http://localhost:4173"));
