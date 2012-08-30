marktex
=======

Markdown風の文書をtexコードに変換するプログラム

##使い方
以下の命令を実行します．

% python src/marktex.py test/test.md

するとout.texが生成されます．この時エンコーディングはUTF-8ですのでtex環境にあわせてエンコーディングを変更します

例 to Shift JIS

% nkf --overwrite -Ws test/out.tex
