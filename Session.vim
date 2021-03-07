let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Documents/Git/tuc-django/tuc
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
argglobal
%argdel
edit templates/article.html
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 88 - ((7 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
88
normal! 0155|
tabnext 1
badd +84 templates/article.html
badd +47 users/views.py
badd +36 article/views.py
badd +6 article/urls.py
badd +12 templates/signin.html
badd +10 social_login/views.py
badd +2 social_login/urls.py
badd +24 tuc/urls.py
badd +25 templates/index.html
badd +226 website/views.py
badd +6 users/urls.py
badd +0 social_login/apps.py
badd +3 social_login/models.py
badd +0 social_login/tests.py
badd +35 tuc/settings.py
badd +0 templates/profile_picture.html
badd +55 templates/base.html
badd +0 users/tests.py
badd +0 users/apps.py
badd +0 users/admin.py
badd +4 website/context_processors.py
badd +37 article/models.py
badd +0 article/templatetags/__init__.py
badd +10 ~/Documents/Git/tuc-django/tuc/article/templatetags/custom_filters.py
badd +74 ~/Documents/Git/tuc-django/tucVirtualEnv/lib/python3.8/site-packages/django/utils/timesince.py
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToOS
set winminheight=1 winminwidth=1
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
