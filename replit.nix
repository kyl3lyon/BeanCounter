{ pkgs }: {
  deps = [
    pkgs.openssl
    pkgs.postgresql
    pkgs.glibcLocales
    pkgs.tree
  ];
}