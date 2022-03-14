#!/bin/sh

# This is just a small sh script to generate the Sog release binaries

export GOARCH=386
for GOOS in android darwin freebsd netbsd openbsd plan9 windows linux; do
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o sog-${GOOS}-x86 ..
    md5sum sog-${GOOS}-x86
done

export GOARCH=amd64
for GOOS in android darwin freebsd netbsd openbsd plan9 solaris windows linux; do
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o sog-${GOOS}-${GOARCH} ..
    sha256sum sog-${GOOS}-${GOARCH}
done

export GOARCH=arm
for GOOS in android darwin freebsd netbsd openbsd plan9 windows linux; do
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o sog-${GOOS}-${GOARCH} ..
    sha256sum sog-${GOOS}-${GOARCH}
done

export GOARCH=arm64
for GOOS in android darwin freebsd illumos netbsd openbsd linux; do
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o sog-${GOOS}-${GOARCH} ..
    sha256sum sog-${GOOS}-${GOARCH}
done

GOOS=linux
for GOARCH in mips mips64 mips64le mipsle ppc64 ppc64le s390x; do
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o sog-${GOOS}-${GOARCH} ..
    sha256sum sog-${GOOS}-${GOARCH}
done

echo Building Dio for ${GOOS}-ARMv6
GOARCH=arm GOARM=6 go build -o sog-${GOOS}-armv6 ..
sha256sum sog-${GOOS}-armv6

echo Building Dio for aix-ppc64
go build -o sog-aix-ppc64 ..
sha256sum sog-aix-ppc64

echo Building Dio for js-wasm
go build -o sog-js-wasm ..
sha256sum sog-js-wasm
