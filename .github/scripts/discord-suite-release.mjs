// Explicit dispatch only, after the suite assets have been downloaded and verified.
import fs from 'node:fs';
const release=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
if(release.isDraft || !/^v\d+\.\d+\.\d+$/.test(release.tagName))throw new Error('Published suite release required');
const assets=release.assets.filter(a=>/\.zip$|\.json$|^SHA256SUMS$/.test(a.name));
if(assets.length<6)throw new Error('Suite assets incomplete');
const lines=assets.map(a=>`[${a.name}](${a.url})`);
const description=[release.isPrerelease?'**Предварительный релиз:** полный smoke-test новой кампании и загрузки сохранения ещё не выполнен.':'',
  `[Страница релиза и изменения](${release.url})`,'',...lines,'',
  'Скачайте все ZIP комплекта. Если пакет разбит на part01/part02, нужны все его части: распакуйте их в один каталог Mods. Склеивать архивы не нужно.'].filter(x=>x!==null).join('\n');
if(description.length>4096)throw new Error('Discord description too long');
const payload={allowed_mentions:{parse:[]},embeds:[{title:release.name,url:release.url,description,color:0xb49a60}]};
if(process.argv.includes('--dry-run')){console.log(JSON.stringify(payload,null,2));process.exit(0);}
const url=new URL(process.env.DISCORD_WEBHOOK_URL);
if(url.protocol!=='https:'||!['discord.com','discordapp.com'].includes(url.hostname)||!url.pathname.startsWith('/api/webhooks/'))throw new Error('Invalid Discord webhook');
url.searchParams.set('wait','true');
const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
if(!response.ok)throw new Error(`Discord HTTP ${response.status}`);
const message=await response.json();
console.log(JSON.stringify({status:'sent',tag:release.tagName,message_id:message.id,channel_id:message.channel_id}));
