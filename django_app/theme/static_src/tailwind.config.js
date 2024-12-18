// theme/static_src/tailwind.config.js

module.exports = {
    content: [
        // DjangoテンプレートでTailwindを使用する場所
        '../templates/**/*.html',  // themeアプリ内のテンプレート
        './theme/static_src/src/**/*.{html,js}',  // Tailwindのソース

        // プロジェクト全体のテンプレート（必要に応じて追加）
        '../../templates/**/*.html',  // ルートテンプレートディレクトリ
        '../../**/templates/**/*.html',  // 他のアプリのテンプレート（必要に応じて追加）
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
