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
edit website/views.py
set splitbelow splitright
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
2wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
wincmd =
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
let s:l = 23 - ((4 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
23
normal! 012|
wincmd w
argglobal
if bufexists("website/urls.py") | buffer website/urls.py | else | edit website/urls.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 14 - ((6 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
14
normal! 027|
wincmd w
argglobal
if bufexists("templates/article.html") | buffer templates/article.html | else | edit templates/article.html | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 69 - ((5 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
69
normal! 041|
wincmd w
wincmd =
tabnext 1
badd +24 website/views.py
badd +72 templates/article.html
badd +47 users/views.py
badd +13 article/views.py
badd +6 article/urls.py
badd +12 templates/signin.html
badd +10 social_login/views.py
badd +2 social_login/urls.py
badd +36 tuc/urls.py
badd +25 templates/index.html
badd +6 users/urls.py
badd +1 social_login/apps.py
badd +3 social_login/models.py
badd +1 social_login/tests.py
badd +35 tuc/settings.py
badd +1 templates/profile_picture.html
badd +1 templates/base.html
badd +1 users/tests.py
badd +1 users/apps.py
badd +1 users/admin.py
badd +4 website/context_processors.py
badd +42 article/models.py
badd +1 article/templatetags/__init__.py
badd +10 ~/Documents/Git/tuc-django/tuc/article/templatetags/custom_filters.py
badd +74 ~/Documents/Git/tuc-django/tucVirtualEnv/lib/python3.8/site-packages/django/utils/timesince.py
badd +1 templates/articles/aj.html
badd +9 a.html
badd +17 website/urls.py
badd +1 templates/edit.html
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
