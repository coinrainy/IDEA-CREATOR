#!/usr/bin/env python3
"""Lightweight CUDA activity loop for keeping a remote GPU session alive."""

import argparse
import os
import signal
import sys
import time

import torch


STOP = False


def _handle_stop(signum, frame):
    del signum, frame
    global STOP
    STOP = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--size", type=int, default=1024)
    parser.add_argument("--interval", type=float, default=8.0)
    parser.add_argument("--active-seconds", type=float, default=0.6)
    parser.add_argument("--log-every", type=int, default=10)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available; cannot start GPU keepalive.")

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    device = torch.device(args.device)
    torch.cuda.set_device(device)
    a = torch.randn((args.size, args.size), device=device)
    b = torch.randn((args.size, args.size), device=device)
    c = torch.empty((args.size, args.size), device=device)
    torch.cuda.synchronize(device)

    print(
        f"[gpu_keepalive] pid={os.getpid()} device={device} "
        f"name={torch.cuda.get_device_name(device)} size={args.size} "
        f"interval={args.interval}s active={args.active_seconds}s",
        flush=True,
    )

    loops = 0
    while not STOP:
        loops += 1
        deadline = time.monotonic() + args.active_seconds
        ops = 0
        while time.monotonic() < deadline and not STOP:
            torch.mm(a, b, out=c)
            a, c = c, a
            ops += 1
        torch.cuda.synchronize(device)
        if loops == 1 or loops % args.log_every == 0:
            allocated = torch.cuda.memory_allocated(device) / (1024 ** 2)
            print(
                f"[gpu_keepalive] loop={loops} ops={ops} "
                f"allocated_mib={allocated:.1f}",
                flush=True,
            )
        sleep_for = max(0.0, args.interval - args.active_seconds)
        end_sleep = time.monotonic() + sleep_for
        while time.monotonic() < end_sleep and not STOP:
            time.sleep(min(1.0, end_sleep - time.monotonic()))

    print("[gpu_keepalive] stopping", flush=True)


if __name__ == "__main__":
    main()
