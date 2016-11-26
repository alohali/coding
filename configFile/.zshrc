# Path to your oh-my-zsh installation.
export ZSH=/home/alohal/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="gentoo"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

# User configuration

export ANDROID_SDK="/home/utils_local/android/android-sdk-linux"
export ANDROID_NDK="/home/utils_local/android/android-ndk-r10e"
export AMDAPPSDKROOT="/opt/AMDAPPSDK-3.0-0-Beta"
export SWIG_ROOT="/home/tools/swig-3.0.6"
export CUSTOM_GO="/usr/local/go"
export PATH="$PATH:$CUSTOM_GO/bin:$SWIG_ROOT/bin:$ANDROID_SDK/platform-tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
export LD_LIBRARY_PATH="$AMDAPPSDKROOT/lib/x86_64/sdk:$AMDAPPSDKROOT/lib/x86/sdk:$LD_LIBRARY_PATH"
# export MANPATH="/usr/local/man:$MANPATH"
source $ZSH/oh-my-zsh.sh

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/dsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias p4="/home/utils/p4-2013.1/bin/p4"
alias tr="tmux attach-session -d -t"
alias sudo="sudo env PATH=$PATH"
alias v='vim'
alias vi='vim'
alias rm='rm -i'  
alias cp='cp -i'  
alias mv='mv -i'  
# -> Prevents accidentally clobbering files.  
alias mkdir='mkdir -p'  
#-------------------------------------------------------------  
alias h='history'  
alias j='jobs -l'  
alias which='type -a'  
alias ..='cd ..'  
#-------------------------------------------------------------  
# Pretty-print of some PATH variables:  
alias path='echo -e ${PATH//:/\\n}'  
alias libpath='echo -e ${LD_LIBRARY_PATH//:/\\n}'  
#-------------------------------------------------------------  
alias du='du -kh'    # Makes a more readable output.  
alias df='df -kTh'  
#  
#-------------------------------------------------------------  
# The 'ls' family (this assumes you use a recent GNU ls).  
#-------------------------------------------------------------  
# Add colors for filetype and  human-readable sizes by default on 'ls':  
alias ls='ls -hF --color'  
alias lx='ls -lXB'         #  Sort by extension.  
alias lk='ls -lSr'         #  Sort by size, biggest last.  
alias lt='ls -ltr'         #  Sort by date, most recent last.  
alias lc='ls -ltcr'        #  Sort by/show change time,most recent last.  
alias lu='ls -ltur'        #  Sort by/show access time,most recent last.  
alias l='ls -CF'        #  Sort by/show access time,most recent last.  
#  
# The ubiquitous 'll': directories first, with alphanumeric sorting:  
alias ll="ls -lv --group-directories-first"  
alias lm='ll |more'        #  Pipe through 'more'  
alias lr='ll -R'           #  Recursive ls.  
alias la='ll -A'           #  Show hidden files.  
alias tree='tree -Csuh'    #  Nice alternative to 'recursive ls' ...  
#-------------------------------------------------------------  
alias dir="ls"                      # 模拟windows  
alias lrd="ls -lR|grep '^[dl]'"     # 递归列出所有的目录,包括链接  
alias lsd="ls -l|grep '^[dl]'"     # 列出所有的目录,包括链接  
#-------------------------------------------------------------  
#  
# My System Environment Variables  
#-------------------------------------------------------------  
# $MYDIR and $MYLOCAL For most application installer  

export PATH=$PATH:/usr/local/cuda-8.0/bin/:/home/alohal/apic
export LD_LIBRARY_PATY=$LD_LIBRARY_PATH:/usr/local/cuda-8.0/lib64:/home/alohal/mount/dittree/sw/gpgpu/MachineLearning/DIT/dev/externals/cudnn-linux/lib64/:/home/alohal/mount/dittree/sw/gpgpu/MachineLearning/DIT/externals/winograd-linux/lib/x64/:/home/alohal/mount/dittree/sw/gpgpu/MachineLearning/DIT/externals/cudnn-aarch64/lib64:/home/alohal/mount/dittree/sw/gpgpu/MachineLearning/DIT/trunk/build-cuda-8.0/drivepx2:/home/alohal/mount/dittree/sw/gpgpu/MachineLearning/DIT/externals/protobuf-drivepx/


export _CUDAPROF_INTERNAL=1
export __CUDA_PM_INTERNAL=1
