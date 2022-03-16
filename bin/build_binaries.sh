#!/usr/bin/bash bash
# -*- coding: utf-8 -*-
export GOARCH=386
for GOOS in android darwin freebsd netbsd openbsd plan9 windows linux; do
    export GOOS=${GOOS}
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o ./misc/sog-${GOOS}-x86
done

export GOARCH=amd64
for GOOS in android darwin freebsd netbsd openbsd plan9 solaris windows linux; do
    export GOOS=${GOOS}
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o ./misc/sog-${GOOS}-${GOARCH}
done

export GOARCH=arm
for GOOS in android darwin freebsd netbsd openbsd plan9 windows linux; do
    export GOOS=${GOOS}
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o ./misc/sog-${GOOS}-${GOARCH}
done

export GOARCH=arm64
for GOOS in android darwin freebsd illumos netbsd openbsd linux; do
    export GOOS=${GOOS}
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o ./misc/sog-${GOOS}-${GOARCH}
done

GOOS=linux
for GOARCH in mips mips64 mips64le mipsle ppc64 ppc64le s390x; do
    export GOOS=${GOOS}
    echo Building Dio for ${GOOS}-${GOARCH}
    go build -o ./misc/sog-${GOOS}-${GOARCH}
done

echo Building Dio for ${GOOS}-ARMv6
GOARCH=arm GOARM=6 go build -o ./misc/sog-${GOOS}-armv6

echo Building Dio for aix-ppc64
go build -o ./misc/sog-aix-ppc64

echo Building Dio for js-wasm
go build -o ./misc/sog-js-wasm
