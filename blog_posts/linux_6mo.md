# Title ideas

Themes to hit:
- Linux/Unix
- Software development
- Old Windows, Mac hardware
- Startup

# Story / Context
I have an old Windows laptop from S6 but I'm liking Windows less and less. Some of this is related to bad experiences from Dell-forced software on the system. Some of this is due to the things like Windows Recall. Other times I was feeling that I'd rather setup Linux than figure out more workarounds for WSL. Some of it is simply unknown, like weird audio blips. Around June I started dual-booting between Windows 11 and Kubuntu 24.04 LTS. Then in October I switched to tri-boot, adding Ubuntu 25.10.

I also have a very old Macbook Pro (2014, Intel-based) that has long since stopped getting OS updates. It's so old that Chrome stopped updating for that OS version. Docker stopped updating for it. And I even had problems doing development because DuckDB stopped supporting it. The install process tried to compile it, but failed after 4 hours and there wasn't a quick fix.

# Overall take

## Dell
Ubuntu feels better for software development than Windows 11. Sometimes I have minor issues but most are solvable. Ubuntu 25.10 feels better to me than Kubuntu 24.04.

## Macbook
Ubuntu has given the machine new life. I had to stop using it for startup work once we started using DuckDB due to the incompatibility, but now I have have it running scripts overnight or I can develop at coffee shops. I haven't gone and wiped the OS X partition because I don't need the space but eventually I will.

# Issues experienced and overcome

## vscode (multiple issues)
Initially I was using vscode on Kubuntu, installed via Snap. I had the following issues:
- Some of the save dialogs would crash kdialog repeatedly
- Dragging windows across monitors would often make vscode think I was trying to drag and drop Chrome windows into the cursor position, which sometimes got vscode into bad states
- I had some issues with vscode remembering logins initially and I forget how I resolved that

Current setup: Installed via .deb on Ubuntu.

I haven't had any issues in this setup.

## Chrome triggering settings
This is a known bug, where the first launch of Chrome triggers KDE's settings panel to pop up. I saw that there might be some workarounds but it wasn't worth the effort, just a minor annoyance.

This hasn't been a problem on Ubuntu.

## Slack losing logins
Initially I had this problem on Kubuntu, then after some work with the password manager it resolved. Then once I switched to Ubuntu the issue came back! None of the guides I found about ensuring that Slack (Snap) could access the keyring worked.

What worked was switching from a Snap package to a Flatpak package. That also has the benefit of loading a little faster.

Tried, but didn't work:
I manually connected to the password manager and verified it was connected but it didn't access it:
`sudo snap connect slack:password-manager-service`
`snap connections slack | grep password-manager-service`

I also tried clearing the cache and made sure it was updated.

## Spotify losing logins
I don't remember how I resolved this. 

## Dell-specific

### Windows repartitioning
I didn't want to jump right from Kubuntu 24 to Ubuntu 25 because I couldn't afford to lose several days of work. So I needed to free up some more disk space from the Windows partition to do it. That took me through several frustrating things and I still have lots of unused disk space that I can't use, but it's good enough for now.

ADD DETAILS

## Macbook setup

### Freeing up space
Freeing up space took a little effort because this machine is so old that a prior OS X upgrade created a new partition of everything years ago and I never deleted it. So my first step was to realize that and free up a partition. Perplexity was helpful for this.

### Getting Ubuntu installed
The system is very picky about the USB drive. What worked:
- Formatting as MS‑DOS (FAT) with GUID Partition Map in Disk Utility (other formats run on my other computer were not recognized) [link](https://discourse.ubuntu.com/t/create-a-bootable-usb-stick-on-macos/14016)
- dd to flash the iso (steps below)
- Boot with Option held down and choose EFI Boot.


I followed [these steps](https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command/) to flash the ISO.
```
# 1) List disks and identify your USB (e.g., /dev/disk2)
/usr/sbin/diskutil list

# 2) Unmount the whole USB device (not just a partition)
/usr/sbin/diskutil unmountDisk /dev/diskN

# 3) Write the ISO to the raw device for speed (DANGER: correct N!)
sudo dd if=/path/to/ubuntu-desktop.iso of=/dev/rdiskN bs=1m

# 4) Ensure buffers are flushed, then eject
sync
/usr/sbin/diskutil eject /dev/diskN
```

The steps above were maybe the 4th attempt. On previous attempts, either the USB wasn't listed in the boot menu or else it was listed but booting from it would just hang.

Also note that there were some light visual glitches when booted from USB but those issues didn't persist after installing it to disk.

### Wifi drivers
Ubuntu doesn't come with wifi drivers for the Broadcom BCM4360 chip. So I ordered a cheap USB Ethernet adapter and used it to test Ubuntu when booted from USB and then later I used it again to install wifi chip drivers.

When installing Ubuntu I made sure to select additional drivers, which I think enabled the restricted package source. Some guides say you need to add that explicitly but I didn't need to.

Then: `sudo apt install broadcom-sta-dkms` (Guides suggested an older package name that didn't exist anymore "bcmwl-kernel-source")

Then I rebooted and it just worked!

### Webcam drivers
The guides were good about this and it worked smoothly. The hardware names I saw were "FaceTime HD webcam" and "Broadcom 1570 PCIe".

- Double-check the hardware model against the guide you're following. In my case `lspci -nn | grep -i 1570`
- Install prerequisites: `sudo apt install linux-headers-generic build-essential git curl cpio xz-utils`
- Install firmware: `git clone https://github.com/patjak/facetimehd-firmware.git && cd facetimehd-firmware && make && sudo make install`
- Install driver: `git clone https://github.com/patjak/bcwc_pcie.git && cd bcwc_pcie && make && sudo make install && sudo depmod`
- Load the driver: `sudo modprobe facetimehd` and verify in a one-person video call

Sources:
- [link](https://andreafortuna.org/2024/08/24/from-faceless-to-facetime-installing-webcam-drivers-on-a-debian-powered-macbook-air)
- [link](https://gist.github.com/johnjeffers/3006011ec7767a4101cdd118e8d64290)

### Red light shined through the audio jack

Sometimes I'd have a red light shining through the audio jack.

> That red light shining through your MacBook’s headphone jack is the optical digital audio (TOSLINK / S/PDIF) output, which shares the same jack as the analog output on older Mac models like the 2014 MacBook Pro. When the light turns on, it means the hardware has switched the port into optical mode.

Steps to resolve:
- Run `alsamixer`
- Press F6 to pick your sound card, navigate to S/PDIF, IEC958, or Digital Output channels, then press M to mute.
- Run `sudo alsactl store`

I haven't had problems since.

### Battery life
Short version: TLP works well without additional customization. My other efforts were not successful.

Initially I wanted low-effort monitoring in the top bar. That led me to PowerTracker.
- Setup Gnome extensions and install PowerTracker [link](https://www.ubuntumint.com/powertracker-ubuntu-battery-life-monitor/)
- Manually edit `~/.local/share/gnome-shell/extensions/marcs14@gmail.com/metadata.json` to allow it in Gnome 49, then relogin. This isn't normally needed, but the extension hadn't been updated when I installed Ubuntu 25.10 with Gnome 49

After baselining for a few days I installed TLP, which is a common all-in-one package to optimize battery life. I've found that battery life while sleeping seems better, and it's a little better during normal usage (compared to balanced power mode all the time). I haven't actually noticed any major trends in PowerTracker, so that may have been a poor choice for monitoring. 

```
sudo apt install tlp
sudo tlp start
```

#### Hardware video acceleration
This hardware has Intel Iris 5100 and can do hardware acceleration of h264 video.

I spent some time trying to get hardware video acceleration working for Youtube but I wasn't able to improve battery life that way.
- Didn't get it working in Chrome (using the deb package)
- Got it working in Firefox/Flatpak BUT when I benchmarked it against Chrome, the battery usage was similar.

If you're looking for steps, I think this is what worked:
`sudo apt install vainfo libva-intel-driver`

Then I could confirm that it saw the i965 chip with `vainfo`:

    libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/i965_drv_video.so
    libva info: Found init function __vaDriverInit_1_22
    libva info: va_openDriver() returns 0
    vainfo: VA-API version: 1.22 (libva 2.22.0)
    vainfo: Driver version: Intel i965 driver for Intel(R) Haswell - 2.4.1

Firefox setup:
```
flatpak install flathub org.mozilla.firefox
flatpak run org.mozilla.firefox
```

Then run `flatpak info org.mozilla.firefox` and note the version number under runtime or SDK. In my case it's 24.08.

I also had to install these:
```
flatpak install flathub org.freedesktop.Platform.ffmpeg-full//VERSION
flatpak install flathub org.freedesktop.Platform.VAAPI.Intel//VERSION
```

If you don't specify the version, you can pick it from a list.

And because my hardware only accelerates h264, I installed h264ify to force Youtube to use H264 streams rather than VP9/AV1 (because only h264 is supported by i965).

Older online guides said I'd need to edit Firefox settings but that's no longer needed.

intel-gpu-top is useful for confirming that it's working. To install:
`sudo apt install intel-gpu-tools`

Then run the top ocmmand while playing a video and confirm that there's non-zero usage in the Video row:
`sudo intel_gpu_top`

# Issues not yet resolved

## Bluetooth keyboard lag
I think this happens when my keyboard "wakes up". Somewhere in the middle of typing it'll lead to something like thiiiiiiiiiis. The issue doesn't happen with a wired keyboard but I don't like the feel of the one I have.

## Network multiplexing
If I'm downloading a large file, particularly if I'm syncing tables over to DuckDB, then it really doesn't load webpages quickly. On Windows that was less of a problem. I'm assuming Windows does some sort of fancy network multiplexing.

## Civ 6
I briefly tried getting Civ 6 working in Steam under Kubuntu 24.04 but I couldn't get that working. I may try again soon.

## Multi-monitor fractional scaling
For my Dell, the laptop monitor has pretty high DPI compared to my external monitor. That mades text difficult to read. But if I set fractional scaling to the same on both monitors, the text is too big on the external monitor. In Windows, I like to have the laptop screen at 125% and the external monitor at 100%.

That wasn't supported in Kubuntu 24, and is glitchy in Ubuntu 25. The glitches are bad enough that I just deal with it and don't put much on the laptop screen.

## Spotify audio blips
I think I switched to Spotify via deb rather than Snap, and it sometimes has the audio cut out. I haven't figured it out.

## Wake speed (Macbook)
On OS X, my Macbook would wake from sleep in about 1 second. On Ubuntu, it takes maybe 10 seconds.

I can see the options in here:
```
> cat /sys/power/mem_sleep
s2idle [deep]
```

Then changed it to s2idle:
```echo s2idle | sudo tee /sys/power/mem_sleep```

Sadly that drainged the battery overnight, so I'll just live with the slower waking.

## Battery health saver
TLP has some pointers on how to set this up with Apple silicon (M chips) but not Intel. That said, I've noticed that it tends to stop at around 95% which is good enough for me.

