#!/bin/bash

echo "🚀 SynergyFlow を起動します..."

# バックエンドとフロントエンドを並列で起動
cd synergyflow-api && npm run start:dev &
API_PID=$!

cd ../synergyflow-client && npm run dev &
CLIENT_PID=$!

echo ""
echo "✅ サーバーを起動しました"
echo "バックエンド: http://localhost:3000 (PID: $API_PID)"
echo "フロントエンド: http://localhost:3001 (PID: $CLIENT_PID)"
echo ""
echo "停止するには Ctrl+C を押してください"

# シグナルをトラップして、両方のプロセスを終了
trap "kill $API_PID $CLIENT_PID; exit" INT TERM

# プロセスが終了するまで待機
wait

