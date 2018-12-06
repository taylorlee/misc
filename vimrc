" TODO
" try deoplete
    " https://github.com/Shougo/deoplete.nvim
" autocommand groups

set nocompatible              " be iMproved, required
filetype off                  " required
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

"PluginInstall
Plugin 'gmarik/Vundle.vim'

"useful text objects
Plugin 'kana/vim-textobj-indent'
Plugin 'kana/vim-textobj-user'
Plugin 'bps/vim-textobj-python'

"syntax
Plugin 'vim-syntastic/syntastic'
"Plugin 'w0rp/ale'
Plugin 'rust-lang/rust.vim'
Plugin 'pangloss/vim-javascript'

"statusline
"Plugin 'vim-airline/vim-airline'

"search
Plugin 'junegunn/fzf'
Plugin 'junegunn/fzf.vim'
Plugin 'mileszs/ack.vim'

"completion
Plugin 'racer-rust/vim-racer'
Plugin 'Valloric/YouCompleteMe' " completion

"misc
Plugin 'altercation/vim-colors-solarized'
Plugin 'scrooloose/nerdtree'
Plugin 'tpope/vim-fugitive'     " git
Plugin 'godlygeek/tabular'      " formatting alignment
Plugin 'mattn/webapi-vim'       " for downloading things

"explore: maybe fit into vim workflow?
"Plugin 'kana/vim-arpeggio'      " chords
"Plugin 'mattn/emmet-vim'        " text expansion

"operators: 
"Plugin 'kana/vim-operator-user'
"Plugin 'tpope/vim-surround'
"Plugin 'rhysd/vim-operator-surround'


call vundle#end()            " required

filetype plugin indent on    " required

let mapleader = "\<Space>"

set undofile
set undodir=~/.vim/undodir

set clipboard=unnamedplus

map <Leader>n :NERDTreeToggle<CR>

"ALE
" rls is slower than cargo!

"let g:airline#extensions#ale#enabled = 1

"let g:ale_completion_enabled = 1 "needs rls
"let g:ale_lint_on_text_changed = 'never'
"let g:ale_open_list = 1
"" uses loclist! need to close quickfix/loclist
"let g:ale_list_window_size = 5

set hidden
let g:racer_cmd = "/home/taylor/.cargo/bin/racer"
let g:racer_experimental_completer = 1

"SYNTASTIC
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 0
let g:syntastic_check_on_wq = 0

let g:syntastic_rust_checkers = ['cargo']
let g:syntastic_python_checkers = ['pyflakes']

"Youcompleteme
let g:ycm_rust_src_path = '/home/taylor/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/src/rust/src'
let g:ycm_autoclose_preview_window_after_insertion = 1

"backups
set nobackup
set nowritebackup

"opening
nnoremap  <Leader>ot :tabe **/
nnoremap  <Leader>os :vs **/

"saving
nnoremap <Leader>w :w<CR>
nnoremap <Leader>z :wq<CR>
nnoremap <Leader>q :lclose <bar> q<CR>


"searching
set incsearch
set hlsearch
set ignorecase
set smartcase
noremap <Leader><Esc> :nohlsearch <bar> lclose<CR>
map <Leader>g :Ack <cword><CR>
vnoremap // y/<C-R>"<CR>

let g:ackprg = 'rg --vimgrep --no-heading'
"command! -bang -nargs=* Rg
      "\ call fzf#vim#grep(
      "\   'rg --column --line-number --no-heading --color=always --ignore-case '.shellescape(<q-args>), 1,
      "\   <bang>0 ? fzf#vim#with_preview('up:60%')
      "\           : fzf#vim#with_preview('right:50%:hidden', '?'),
      "\   <bang>0)

""tags
"set tags=./tags,tags;

set shellcmdflag=-ic

function MkTags()
    execute "! clear; mkctags"
    "set shellcmdflag=-c
    return
endfunction
nnoremap <Leader>r :call MkTags()<CR>

nnoremap <Leader>T :execute "tabe " . "templates/<cfile>"<CR> 
"nnoremap <Leader>T :execute "tabe " . djroot . "/penny/templates/<cfile>"<CR>

"splitting
set splitright
nnoremap <Leader>] :vsp <CR>:exec("tag ".expand("<cword>"))<CR>

"splits nav like tmux nav
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>


"testing
let djroot = "/home/taylor/eclosion"
function GetTest()
    "set shellcmdflag=-ic
    let djroot = "/home/taylor/eclosion"
    let prefix =" cd " . djroot . "; workon eclosion; py.test -s -k"
    let full = "! clear; " . prefix . "<cword>"
    execute full
    "set shellcmdflag=-c
    return
endfunction

"compiling
set autowrite
nnoremap <Leader>m :! clear; make<CR>

"yanking/pasting
nnoremap <Leader>a :%y<CR>

"formatting
set expandtab
set autoindent
set number
vmap <Leader>t :Tabularize /
vmap <Leader>s :sort ui<Esc>
vnoremap > ><CR>gv 
vnoremap < <<CR>gv

"(python) string-listify selected rows:
let @s = "i'$a',"
vnoremap <Leader>sl :norm! @s<CR>o]<ESC>{O[<ESC>

"colors
syntax on 
let g:solarized_termcolors=256

if system("vim_bg_color") == "light"
    set background=light
else
    set background=dark
endif

colorscheme solarized

nnoremap <Leader><C-d> :set background=dark<CR>
nnoremap <Leader><C-l> :set background=light<CR>

"fugutive
nnoremap <Leader>b :Gblame<CR>
nnoremap <Leader>gh v:Gbrowse!<CR>

"debugger
autocmd FileType python nnoremap <Leader>i oimport ipdb; ipdb.set_trace()<Esc>
autocmd FileType javascript nnoremap <Leader>i odebugger;<Esc>

"linter
autocmd FileType python nnoremap <Leader>l :w<CR>:! clear; pyflakes %<CR>
autocmd FileType javascript nnoremap <Leader>l :w<CR>:! clear; eslint --quiet %<CR>
autocmd FileType rust nnoremap <Leader>l :w<CR>:! clear; cargo clippy<CR>

"formatter
autocmd FileType javascript set formatprg=prettier\ --stdin
autocmd FileType python set formatprg=yapf
autocmd FileType python nnoremap <Leader>f :! clear; yapf -i %;<CR>:edit<CR>
autocmd FileType rust set formatprg=rustfmt
autocmd FileType rust nnoremap <Leader>f :! cargo fmt<CR>:edit<CR>

"docstrings
autocmd FileType python nnoremap <leader>d o'''<CR>'''<Esc>k$a
autocmd FileType javascript nnoremap <leader>d o//

"comments 
autocmd FileType python noremap <Leader>c :s/\(^\s*\)\(\S\)/\1#\2/<CR> :nohlsearch<CR>
autocmd FileType python noremap <Leader>u :s/#//<CR>
autocmd FileType javascript noremap <Leader>c :s/\(^\s*\)\(\S\)/\1\/\/\2/<CR> :nohlsearch<CR>
autocmd FileType javascript noremap <Leader>u :s/\/\///<CR>
autocmd FileType vim noremap <Leader>c :s/\(^\s*\)\(\S\)/\1"\2/<CR> :nohlsearch<CR>
autocmd FileType vim noremap <Leader>u :s/"//<CR>
autocmd FileType rust noremap <Leader>c :s/\(^\s*\)\(\S\)/\1\/\/\2/<CR> :nohlsearch<CR>
autocmd FileType rust noremap <Leader>u :s/\/\///<CR>

"TODOs
autocmd FileType python nnoremap <leader>td o#TODO: 
autocmd FileType javascript nnoremap <leader>td o//TODO: 

autocmd FileType rust nnoremap <leader>td o//TODO: 

"testing
"autocmd FileType python nnoremap <Leader>t :call GetTest()<CR>
autocmd FileType python nnoremap <Leader>t :! clear; python3 %<CR>
autocmd FileType ruby nnoremap <Leader>t :! clear; rake <CR>
autocmd FileType rust nnoremap <Leader>t :! clear; cargo test<CR>

"misc
autocmd FileType ruby nnoremap <Leader>n /__<CR>ciw

"tags
autocmd BufRead *.rs :setlocal tags=./rusty-tags.vi;/
autocmd BufWritePost *.rs :silent! exec "!rusty-tags vi --quiet --start-dir=" . expand('%:p:h') . "&" | redraw!
autocmd BufRead *.rs :setlocal tags=./rusty-tags.vi;/,$RUST_SRC_PATH/rusty-tags.vi

"au FileType rust nmap gd <Plug>(rust-def)
"au FileType rust nmap gs <Plug>(rust-def-split)
"au FileType rust nmap gx <Plug>(rust-def-vertical)
"au FileType rust nmap <leader>gd <Plug>(rust-doc)

"spacing
set shiftwidth=4 
set tabstop=4

autocmd FileType yaml setl indentkeys-=<:>
autocmd FileType yaml set shiftwidth=4 
autocmd FileType yaml set tabstop=4

autocmd FileType javascript set shiftwidth=4 
autocmd FileType javascript set tabstop=4

autocmd FileType html set shiftwidth=2 
autocmd FileType html set tabstop=2

autocmd FileType scss set shiftwidth=2 
autocmd FileType scss set tabstop=2 

autocmd FileType python set shiftwidth=4 
autocmd FileType python set tabstop=4

au BufRead,BufNewFile *.yapf set ft=dosini

