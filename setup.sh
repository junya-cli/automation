#!/bin/bash

echo "🚀 SynergyFlow セットアップを開始します..."

# バックエンドのセットアップ
echo ""
echo "📦 バックエンドのセットアップ中..."
cd synergyflow-api

if [ ! -f .env ]; then
  echo "📝 .envファイルを作成中..."
  cp .env.example .env
  echo "⚠️  .envファイルを編集して、DATABASE_URLとJWT_SECRETを設定してください"
else
  echo "✅ .envファイルは既に存在します"
fi

echo "📦 依存関係をインストール中..."
npm install

echo ""
echo "🗄️  Prismaクライアントを生成中..."
npx prisma generate

echo ""
echo "⚠️  データベースを準備してから、以下のコマンドを実行してください:"
echo "   cd synergyflow-api"
echo "   npx prisma migrate dev --name init"

cd ..

# フロントエンドのセットアップ
echo ""
echo "📦 フロントエンドのセットアップ中..."
cd synergyflow-client

if [ ! -f .env.local ]; then
  echo "📝 .env.localファイルを作成中..."
  cp .env.local.example .env.local
  echo "✅ .env.localファイルを作成しました"
else
  echo "✅ .env.localファイルは既に存在します"
fi

echo "📦 依存関係をインストール中..."
npm install

cd ..

echo ""
echo "✅ セットアップが完了しました！"
echo ""
echo "次のステップ:"
echo "1. synergyflow-api/.env を編集して、DATABASE_URLとJWT_SECRETを設定"
echo "2. データベースを準備（PostgreSQLまたはPrisma Postgres）"
echo "3. cd synergyflow-api && npx prisma migrate dev --name init"
echo "4. バックエンドを起動: cd synergyflow-api && npm run start:dev"
echo "5. フロントエンドを起動: cd synergyflow-client && npm run dev"
echo ""
echo "バックエンド: http://localhost:3000"
echo "フロントエンド: http://localhost:3001"

