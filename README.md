# SynergyFlow - 次世代目標達成プラットフォーム

チーム全体の目標設定から個人のタスク実行までをシームレスに連携させ、生産性を最大化する目標達成プラットフォームです。

## 🎯 主な機能

- ✅ **ユーザー認証**: メールアドレスとパスワードによる安全な認証
- ✅ **ワークスペース管理**: チームやプロジェクトごとのワークスペース作成・管理
- ✅ **目標設定（OKR）**: 階層構造での目標設定とKey Resultsによる進捗管理
- ✅ **戦略プランナー**: ツリー構造で戦略やイニシアチブを視覚的に計画
- ✅ **タスクボード**: カンバン形式のタスク管理（ドラッグ＆ドロップ対応）
- ✅ **ダッシュボード**: 目標達成率やタスク進捗をリアルタイムで可視化

## 📁 プロジェクト構成

```
automation/
├── synergyflow-client/  # Next.js フロントエンド
└── synergyflow-api/     # NestJS バックエンド
```

## 🛠️ 技術スタック

### フロントエンド
- **フレームワーク**: Next.js 16 (App Router)
- **言語**: TypeScript
- **スタイリング**: Tailwind CSS
- **状態管理**: Zustand
- **データフェッチ**: TanStack Query (React Query)
- **ドラッグ＆ドロップ**: @dnd-kit/core, @dnd-kit/sortable
- **フォーム**: React Hook Form + Zod
- **UI コンポーネント**: shadcn/ui
- **グラフ**: Recharts

### バックエンド
- **フレームワーク**: NestJS
- **言語**: TypeScript
- **データベース**: PostgreSQL
- **ORM**: Prisma
- **認証**: JWT (JSON Web Token)
- **バリデーション**: class-validator, class-transformer

## 🚀 クイックスタート

### 前提条件
- Node.js 18以上
- PostgreSQL データベース（またはPrisma Postgres）

### 自動セットアップ

```bash
# セットアップスクリプトを実行
chmod +x setup.sh
./setup.sh
```

### 手動セットアップ

#### 1. バックエンドのセットアップ

```bash
cd synergyflow-api

# 環境変数の設定
cp .env.example .env
# .envファイルを編集して、DATABASE_URLとJWT_SECRETを設定

# 依存関係のインストール
npm install

# Prismaクライアントの生成
npx prisma generate

# データベースマイグレーション
npx prisma migrate dev --name init

# 開発サーバー起動
npm run start:dev
```

バックエンドは `http://localhost:3000` で起動します。

#### 2. フロントエンドのセットアップ

```bash
cd synergyflow-client

# 環境変数の設定
cp .env.local.example .env.local
# .env.localファイルを編集して、NEXT_PUBLIC_API_URLを設定（必要に応じて）

# 依存関係のインストール
npm install

# 開発サーバー起動
npm run dev
```

フロントエンドは `http://localhost:3001` で起動します。

### 一括起動

```bash
# バックエンドとフロントエンドを同時に起動
chmod +x start.sh
./start.sh
```

## 📝 環境変数

### バックエンド (.env)

```env
DATABASE_URL="postgresql://user:password@localhost:5432/synergyflow?schema=public"
JWT_SECRET="your-super-secret-jwt-key-change-in-production"
PORT=3000
FRONTEND_URL="http://localhost:3001"
```

### フロントエンド (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## 📚 API エンドポイント

### 認証
- `POST /auth/signup` - ユーザー登録
- `POST /auth/login` - ログイン
- `GET /auth/me` - 現在のユーザー情報取得（認証必須）

### ワークスペース
- `POST /workspaces` - ワークスペース作成
- `GET /workspaces` - ワークスペース一覧取得
- `GET /workspaces/:id` - ワークスペース詳細取得
- `PATCH /workspaces/:id` - ワークスペース更新
- `DELETE /workspaces/:id` - ワークスペース削除
- `POST /workspaces/:id/members` - メンバー招待
- `PATCH /workspaces/:id/members/:memberId/role` - メンバーロール変更
- `DELETE /workspaces/:id/members/:memberId` - メンバー削除

### 目標（OKR）
- `POST /workspaces/:workspaceId/objectives` - 目標作成
- `GET /workspaces/:workspaceId/objectives` - 目標一覧取得
- `GET /workspaces/:workspaceId/objectives/:id` - 目標詳細取得
- `PATCH /workspaces/:workspaceId/objectives/:id` - 目標更新
- `DELETE /workspaces/:workspaceId/objectives/:id` - 目標削除

### 戦略ノード
- `POST /workspaces/:workspaceId/strategy-nodes` - 戦略ノード作成
- `GET /workspaces/:workspaceId/strategy-nodes` - 戦略ノード一覧取得
- `GET /workspaces/:workspaceId/strategy-nodes/:id` - 戦略ノード詳細取得
- `PATCH /workspaces/:workspaceId/strategy-nodes/:id` - 戦略ノード更新
- `DELETE /workspaces/:workspaceId/strategy-nodes/:id` - 戦略ノード削除
- `POST /workspaces/:workspaceId/strategy-nodes/reorder` - ノードの並び替え

### タスク
- `POST /workspaces/:workspaceId/tasks` - タスク作成
- `GET /workspaces/:workspaceId/tasks` - タスク一覧取得
- `GET /workspaces/:workspaceId/tasks/:id` - タスク詳細取得
- `PATCH /workspaces/:workspaceId/tasks/:id` - タスク更新
- `DELETE /workspaces/:workspaceId/tasks/:id` - タスク削除

### ダッシュボード
- `GET /workspaces/:workspaceId/dashboard` - ダッシュボード統計データ取得

## 🗄️ データベーススキーマ

- **User**: ユーザー情報
- **Workspace**: ワークスペース
- **WorkspaceMember**: ワークスペースメンバー
- **Objective**: 目標（OKR）
- **StrategyNode**: 戦略ノード
- **Task**: タスク

詳細は `synergyflow-api/prisma/schema.prisma` を参照してください。

## 🏗️ ビルドとデプロイ

### バックエンド

```bash
cd synergyflow-api
npm run build
npm run start:prod
```

### フロントエンド

```bash
cd synergyflow-client
npm run build
npm run start
```

## 📖 使い方

1. **アカウント作成**: サインアップページで新規アカウントを作成
2. **ワークスペース作成**: ダッシュボードから新しいワークスペースを作成
3. **メンバー招待**: ワークスペースにメンバーを招待（管理者のみ）
4. **目標設定**: ワークスペースでOKRを設定
5. **戦略計画**: 戦略プランナーで目標達成のための戦略を計画
6. **タスク管理**: タスクボードでタスクを作成・管理
7. **進捗確認**: ダッシュボードで全体の進捗を確認

## 🔧 開発

### バックエンドの開発

```bash
cd synergyflow-api
npm run start:dev  # ホットリロード有効
```

### フロントエンドの開発

```bash
cd synergyflow-client
npm run dev  # ホットリロード有効
```

### データベースマイグレーション

```bash
cd synergyflow-api
npx prisma migrate dev --name migration_name
npx prisma studio  # データベースをブラウザで確認
```

## 📄 ライセンス

Private

## 🤝 サポート

問題が発生した場合は、以下の点を確認してください：

1. 環境変数が正しく設定されているか
2. データベースが起動しているか
3. ポート3000と3001が使用可能か
4. 依存関係が正しくインストールされているか
