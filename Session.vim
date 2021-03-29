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
edit extra_user_detail/admin.py
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
let s:l = 83 - ((7 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
83
normal! 014|
wincmd w
argglobal
if bufexists("article/models.py") | buffer article/models.py | else | edit article/models.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 132 - ((6 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
132
normal! 0
wincmd w
argglobal
if bufexists("extra_user_detail/models.py") | buffer extra_user_detail/models.py | else | edit extra_user_detail/models.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 67 - ((3 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
67
normal! 05|
wincmd w
2wincmd w
wincmd =
tabnext 1
badd +80 website/views.py
badd +95 templates/article.html
badd +304 templates/new.html
badd +675 ~/.vimrc
badd +81 article/admin.py
badd +131 article/models.py
badd +70 extra_user_detail/models.py
badd +40 extra_user_detail/admin.py
badd +3 curd/models.py
badd +41 website/urls.py
badd +6 article/urls.py
badd +24 article/views.py
badd +0 extra_user_detail/views.py
badd +8 users/views.py
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
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
