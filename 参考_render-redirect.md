## render
### renderの使い方

関数ベースビューならこれを多用する。
HttpResponseの特定の機能を盛り込んだショートカット関数です。

HttpResponseではテンプレートを表示する際に
Django.templateモジュールのloaderなどを
引っ張ってくる必要がありますが、

renderでは第２引数でテンプレートを表示でき
第３引数で文字列などのデータを渡すことができます。

```
def sample(request):
    context = {'sample':'この文字を引き渡す'}
    return render(request, sample.html, context)
```


## redirect
### redirectの使い方	
    
読み方通りのリダイレクトであり	
Webページに来たユーザを別のURLに転送する。	
    
例えばフォーム入力が完了した際に元のページに戻る際に使われたり	
今までのURLを残したまま、リニューアルしたURLへ転送する時に使われる。	
(URLでお気に入り登録したユーザなどが混乱しないように)	
    
redirectには３つの特徴があります。	
    
#### 1. 転送先は、絶対URLか相対URL、urls.pyのview名で設定できる	

```
def rel(request):	
    return redirect('/some/url/') #相対URL	
    
def abs(request):	
    return redirect('https://example.com/') #直接URL	
    
def name(request):	
    return redirect('viewname') #view名	
```
 
#### 2. view名で設定した場合、引数も付属してリダイレクトすることができる	

```
def name(request):	
    ...	
    return redirect('viewname', hoge='hoge')	
```

#### 3. モデルのidやuuidを使ったURLを使いたい場合	

models.pyのget_absolute_url()にも対応している	
    

    
