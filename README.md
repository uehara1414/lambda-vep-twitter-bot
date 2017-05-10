# lambda-vep-twitter-bot

[twitter-war-resistant](https://github.com/uehara1414/twitter-war-resistant)の AWS Lambda & Google Spreadsheets 版です  
引用リツイートされたツイート一覧はこちらから閲覧できるようになりました。
https://docs.google.com/spreadsheets/d/1Q3vPjJmot3gYf552_3r6g2qPbMIFHbQ8lvuf2Q1qh70/edit?usp=sharing

## Deploy
1. Google Spreadsheets 利用のためにclient_secret.jsonを作成してください。
手順は[こちら](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
2. `./package.sh`
3. AWS Lambda 上記で作成した lambda-package.zip をアップロード
4. 以下の環境変数を設定
```commandline
UEHARA_CONSUMER_KEY
UEHARA_CONSUMER_SECRET
UEHARA_ACCESS_TOKEN
UEHARA_ACCESS_SECRET
TSUGUMI_CONSUMER_KEY
TSUGUMI_CONSUMER_SECRET
TSUGUMI_ACCESS_TOKEN
TSUGUMI_ACCESS_SECRET
```

あとはお好みでトリガーなどを設定してください。
