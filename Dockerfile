FROM archlinux

RUN pacman -Syu --noconfirm python python-pip python-poetry

RUN pacman -S --noconfirm gawk findutils procps-ng

RUN pacman -S --noconfirm base-devel git

RUN useradd -m builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/builder

USER builder
WORKDIR /home/builder

RUN git clone https://aur.archlinux.org/dafny-bin.git && \
    cd dafny-bin && makepkg -si --noconfirm && \
    cd .. && rm -rf dafny-bin

USER root
WORKDIR /root

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN rustup toolchain install 1.82.0-x86_64-unknown-linux-gnu

RUN pacman -S --noconfirm unzip

RUN curl -L https://github.com/verus-lang/verus/releases/download/release%2F0.2025.03.29.d3b34ce/verus-0.2025.03.29.d3b34ce-x86-linux.zip -O && \
    unzip verus-0.2025.03.29.d3b34ce-x86-linux.zip && \
    rm verus-0.2025.03.29.d3b34ce-x86-linux.zip

ENV PATH="/root/verus-x86-linux:${PATH}"

ENTRYPOINT [ "/bin/sh" ]
