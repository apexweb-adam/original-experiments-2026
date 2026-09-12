from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess
R=Path(__file__).resolve().parent
font='/System/Library/Fonts/Supplemental/Arial.ttf'
def f(n):return ImageFont.truetype(font,n)
W,H,FPS,D=1280,720,24,15
p=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'data-flow.mp4')],stdin=subprocess.PIPE)
pts=[(250,360),(560,270),(560,455),(920,360)]
for frame in range(FPS*D):
 t=frame/FPS;im=Image.new('RGB',(W,H),'#f4f1e9');d=ImageDraw.Draw(im)
 title='Start with the file.' if t<5 else 'Check before you trust.' if t<10 else 'Know what is still owed.'
 d.text((70,48),'DATA FLOW / ORIGINAL MOTION STUDY',font=f(18),fill='#61746b');d.text((70,90),title,font=f(52),fill='#173e35')
 d.text((72,162),'A synthetic invoice journey. Designed and rendered from editable code.',font=f(21),fill='#61746b')
 for a,b,start in [(0,1,1),(0,2,2),(1,3,6),(2,3,7)]:
  x,y=pts[a];xx,yy=pts[b];d.line((x,y,xx,yy),fill='#b8c6bb',width=4)
  if t>start:
   u=min(1,(t-start)/2.4);ex=x+(xx-x)*u;ey=y+(yy-y)*u;d.line((x,y,ex,ey),fill='#24745c',width=5)
   if u<1:d.ellipse((ex-9,ey-9,ex+9,ey+9),fill='#e78646')
 for i,(x,y) in enumerate(pts):
  lift=8*math.sin(min(1,t/1.2)*math.pi/2);y-=lift
  d.polygon([(x-90,y),(x,y-46),(x+90,y),(x,y+46)],fill='#173e35' if i==3 else '#dce5d9')
  d.polygon([(x-90,y),(x,y+46),(x,y+62),(x-90,y+16)],fill='#91b5a2')
  d.polygon([(x,y+46),(x+90,y),(x+90,y+16),(x,y+62)],fill='#397560')
  label=['CSV','IDs','Amounts','Summary'][i];box=d.textbbox((0,0),label,font=f(23));d.text((x-(box[2]-box[0])/2,y-14),label,font=f(23),fill='white' if i==3 else '#173e35')
  sub=['3 demo invoices','Unique IDs','Valid cents','1 pending invoice'][i];box=d.textbbox((0,0),sub,font=f(19));d.text((x-(box[2]-box[0])/2,y+88),sub,font=f(19),fill='#4a6257')
 if t>=10:
  d.rounded_rectangle((790,520,1120,600),radius=10,fill='#173e35');d.text((813,540),'Owed 450.50',font=f(35),fill='white')
 d.line((70,640,1210,640),fill='#cbd4c9',width=2);d.text((70,666),'Original spec sample · no client, product performance or payment claim',font=f(17),fill='#61746b')
 if frame in [48,168,300]:im.save(R/f'frame-{frame}.png')
 p.stdin.write(im.tobytes())
p.stdin.close();code=p.wait();assert code==0,code
print('Rendered 15 seconds, 24 fps, 1280x720; no audio; original procedural graphics.')
