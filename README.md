# OmniPkg

A package manager wrapper for Unix-like systems. It is designed to be a single interface for all package managers, and to be as simple as possible.
Based on [rhinopkg][rhinolin] by [RhinoLinux][rhino].

### Usage
```
USAGE: omni [function] {flag} <input>                                                  

functions:
    install: Install package(s) - Prompts user to respond with 
             the number(s) associated with the desired package(s).
             
    remove:  Uninstall package(s) - Prompts user to respond with
             the number(s) associated with the desired package(s).
             
    search:  Search for package(s) - Does not have a second prompt.
    
    update:  Updates all packages accessible to the wrapper - does
             not accept <input>, instead use install to update 
             individual packages. Has a confirmation prompt.

    cleanup: Attempts to repair broken dependencies and remove any
             unused packages. Does not accept <input>, but has 
             a confirmation prompt.

flags: 
    --help/-h: Display this page
    
    --description/-d: By default, OmniPkg will only display packages 
    that contain <input> within their name. Use this flag to increase 
    range and display packages with <input> in their description.

    -y: Makes functions with confirmation prompts run promptless.
    
input: 
    Provide a package name or description.

Example execution:
    $ omni install foobar
    Found packages matching 'foobar':

    [0]: pyfoobar (apt)
    [1]: foobarshell (apt)
    [2]: foobar (flatpak)
    [3]: foobar-web (snap)
    [4]: foobar-bin (pacstall)
    [5]: foobar-theme (pacstall)

    Select which package to install [0-5]: 3 4 5
    Selecting 'foobar-web' from package manager 'snap'
    Selecting 'foobar-bin' from package manager 'pacstall'
    Selecting 'foobar-theme' from package manager 'pacstall'
    Are you sure? (y/N)
    [...]
```

### Installation
Just download the script and place it in your $PATH. You can also use the following command:
```bash
sudo wget -O /usr/bin/omni https://raw.githubusercontent.com/0mniscient/OmniPkg/master/omni && sudo chmod +x /usr/bin/omni
```

### Supported Package Managers
#### Binary Based (pacman, apt, etc)
Package Manager | Default OS | Supported? | Notes
--- | --- | --- | ---
`apk` | Alpine | Yes |
`apt` | Debian | Yes |
`brew` | MacOS | Yes |
`choco` | Windows | No | TODO
`crew` | ChromeOS | No | TODO
`dnf` | Fedora | Yes |
`emerge` | Gentoo | Yes |
`nix` | Linux | No | TODO
`pacman` | Arch | Yes |
`pkg` | Termux (Android) | Partial | Not recommended
`scoop` | Windows | No | TODO
`winget` | Windows | No | TODO
`xbps` | Void | No | TODO
`yum` | RHEL | Yes |
`zypper` | OpenSUSE | Yes |

#### Container Based (flatpak, snap, docker, distrobox)
Package Manager | Supported? | Notes
--- | --- | ---
`flatpak` | Yes |
`snap` | Yes |
`docker` | No | unlikely to be supported
`distrobox` | No | unlikely to be supported

### Dependencies
- Python 3 

### License
This project is licensed under the GNU GPLv3 License - see the [LICENSE][def] file for details

### Acknowledgments
This is _heavily_ based on RhinoLinux's rhinopkg, which can be found [here][rhino].
I hvae just rebased it to Python 3 and added support for other distros (I am a big fan of Fedora, and I wanted to use this on my Fedora machine instead of trying to figure out which package manager to use for each package).

[def]: LICENSE
[rhino]: https://github.com/RhinoLinux/rhinopkg
[rhinolin]: https://rhinolinux.org/