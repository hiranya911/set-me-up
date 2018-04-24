# Add the following to ~/.bashrc

parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
is_git_dirty() {
  git diff --quiet HEAD &>/dev/null
  [ $? == 1 ] && echo "!"
}

export PS1="\u@\h:\[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[31m\]\$(is_git_dirty)\[\033[00m\] $ "
