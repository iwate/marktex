##使い方
###セクション
2つ以上の\#でセクションを記述できます．
 > \#\#
このように2つの\#でセクションが生成され，以後\#を足すごとにサブセクションが生成されます

###太文字，下線
\#や\_を使い太文字，や下線を引くことができます
> これは\#\#太文字\#\# 
> これは\_\_下線\_\_ 
これは##太文字## \\ 
これは__下線__

###箇条書き
箇条書きは*,+,-を使って記述します
> + ほいさ 
> \ \ \ \ * どっこい 
> \ \ \ \ * よっこいしょ 
> + そいや
このように記述すると次のように出力されます．
+ ほいさ
	* どっこい
	* よっこいしょ
+ そいや
タブで字下げすることで箇条書きも下げられます．

###列挙
数字とピリオドの組み合わせで列挙できます．番号は自動生成されるためすべて1.と書いても列挙して出力されます．
> 1. 1番
> 1. 2番
1. 1番
1. 2番

###自由な箇条書き
数字以外とピリオドの組み合わせで自由に箇条書きのヘッダを記述できます．
> (a). hoge
> (b). fuga
(a). hoge
(b). fuga
このとき，ヘッダは自動でインクリメントされません．

###引用文
$>$を行頭につけるとその行は引用文になります
> $>$ これは $\backslash \backslash$ 
> $>$ 引用文です

> これは
> 引用文です

###画像の添付
画像の添付！から始まり，キャプション，ファイル名と記述します．
> `![hogehoge](img/hoge.eps)`
![hogehgoe](img/hoge.eps)

###ソースコード
ソースコードは3つのグラーブアクセント（｀）から始まり，言語名：キャプションと記述しする．
その後，再び```が出るまでの行をソースコードとして認識します．
> ```java:hoge.java
> public staic void main(string[] args)\{
> \ \ \ \ System.out.println("Hello,World!!");
> \}
> ```

```java:hoge.java
public staic void main(string[] args){
	System.out.println("Hello,World!!");
}
```

### インラインコード
インラインコードはグラーブアクセント（｀）で囲って記述します．	
 > インラインコード｀System.out.println("Hello,World!!");｀です
これは，インラインコード`System.out.println("Hello,World!!");`です

###エスケープ
Texのエスケープに従ってください．
> これは(丸括弧)，これは$\backslash$\{中括弧$\backslash$\}，これは100$\backslash$\%
これは(丸括弧)，これは\{中括弧\}，これは100\%
MarkTexのエスケープは未実装です．つまり半角文字のグラーブアクセントは現在記述できません．他の文字はインラインコードを用いて表記することが可能です．		

###水平線
ハイフン記号を3つ以上つなげることによって水平線が記述できます．
> `---`
---

###スクリーン
アスタリスク（*）を3つ以上で囲むと囲まれた内部がスクリーンに記述されます．	
***************
	hogehogehoe
******************

###アイテムボック
等号（=）で3つ以上で囲むことでアイテムボックスを記述できます．アイテムボックスのヘッダは等号の左，右，または中央に入れることで指定します．
> 左====
> 	hogehogehoe
> =================
左====
	hogehogehoe
=================
> ===右
> 	hogehogehoe
> =================
===右
	hogehogehoe
=================
> ===中央==
> 	hogehogehoe
> =================
===中央==
	hogehogehoe
=================

###数式
eqnarrayをドル記号（\$）3つで囲むことで表現できます．
$$$
a = 0
b = 0
$$$
