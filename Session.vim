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
edit article/views.py
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
let s:l = 74 - ((15 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
74
normal! 0
tabnext 1
badd +83 extra_user_detail/admin.py
badd +154 article/models.py
badd +63 extra_user_detail/models.py
badd +244 website/views.py
badd +303 templates/article.html
badd +304 templates/new.html
badd +675 ~/.vimrc
badd +134 article/admin.py
badd +3 curd/models.py
badd +41 website/urls.py
badd +6 article/urls.py
badd +76 article/views.py
badd +1 extra_user_detail/views.py
badd +111 users/views.py
badd +59 website/context_processors.py
badd +95 tuc/settings.py
badd +23 templates/home.html
badd +7 article/utils.py
badd +0 users/admin.py
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
