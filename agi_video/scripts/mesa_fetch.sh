#!/bin/bash
# mesa_fetch.sh — trixie mesa libs → gllibs/ (manual/idempotent runner)
set -u
TMP=/home/z/my-project/agi_video/agivideo_tmp
GL=$TMP/gllibs
mkdir -p "$GL/extract"
cd "$GL/extract"
curl -s "https://deb.debian.org/debian/dists/trixie/main/binary-amd64/Packages.gz" | gzip -d > P.txt
echo "P.txt: $(wc -c < P.txt) bytes"
PAT='(mesa|libgl1|libegl1|libegl-mesa0|libgbm1|libglx-mesa0|libglapi-mesa0|libdrm2|libdrm-amdgpu1|libdrm-intel1|libdrm-radeon1|libdrm-nouveau2|libdrm-common|libx11-6|libx11-data|libx11-xcb1|libxcb1|libxcb-dri2-0|libxcb-dri3-0|libxcb-glx0|libxcb-present0|libxcb-sync1|libxcb-shm0|libxcb-randr0|libxcb-xfixes0|libxext6|libxfixes3|libxxf86vm1|libxdamage1|libxau6|libxdmcp6|libwayland-client0|libwayland-server0|libwayland-egl1|libwayland-cursor0|libxkbcommon0|libsensors5|libicu76|libxml2|libzstd1|liblzma5|libllvm19|libedit2|libelf1t64|libexpat1|libxshmfence1|libva2|libva-drm2|libva-x11-2|libvdpau1|libvdpau-va-gl1|libnuma1|libudev1|libpciaccess0|libcrypt1|libbsd0|libmd0|libunwind8|libcurl4t64|libbrotli1|libnghttp2-14|librtmp1|libssh2-1t64|libpsl5t64|libldap2|libsasl2-2|libb2-1|libkrb5-3|libk5crypto3|libkeyutils1|libcom-err2|libgssapi-krb5-2|libtinfo6|libmd4c0|libdouble-conversion1|libpcre2-8-0|libglibc2|libc6|libgcc-s1|libstdc++6|libz3-4|libz3-dev|libclang-cpp19|libffi8|libsnappy1v5|libxml2|libicu72)'
rg -A20 "^Package: ($PAT)" P.txt | rg -o '^Filename: \S+\.deb' | awk '{print "http://deb.debian.org/debian/" $2}' | sort -u > debs.txt
echo "debs: $(wc -l < debs.txt)"
while read -r u; do
  f=$(basename "$u")
  [ -s "$f" ] || curl -sL -o "$f" "$u"
done < debs.txt
echo "downloaded: $(ls *.deb 2>/dev/null | wc -l)"
for d in *.deb; do
  dpkg-deb -x "$d" "$GL/" 2>/dev/null || echo "FAIL $d"
done
echo "extracted libs: $(ls $GL/usr/lib/x86_64-linux-gnu/ 2>/dev/null | wc -l)"
ls "$GL/usr/lib/x86_64-linux-gnu/libEGL.so.1" "$GL/usr/lib/x86_64-linux-gnu/libGL.so.1" 2>/dev/null
find "$GL" -name "*mesa*.json" 2>/dev/null
touch "$GL/.done"
