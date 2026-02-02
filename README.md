
# 🚀 HTML 雲端分享中心

這個專案讓你能在戶外透過手機，將朋友傳來的 HTML 程式碼快速發布到 GitHub Pages，生成一個永久且規律命名的靜態連結。

---

## ⏱️ 關於部署時間（一定要看）

- **發布後台（Codespaces）**：即時  
- **公開網頁（GitHub Pages）**：約需 **1～3 分鐘**

每次 `git push` 後，GitHub 會啟動 GitHub Actions 進行建置並同步到全球 CDN。  
請等待 **Actions 圓圈轉完，顯示綠色勾勾 ✅**，公開網址才會更新。

---

## 🛠️ 快速啟動步驟

1. **開啟 Codespaces**  
   GitHub 頁面 → `Code` → `Codespaces`

2. **安裝環境（首次使用）**
   
 ```bash
   pip install flask
```

3. **執行程式**

   ```bash
   python app.py
   ```

4. **開放外部存取**

   * 點擊右下角 `Ports`
   * 找到 `5000` 端口
   * 將 `Visibility` 從 `Private` 改為 `Public`

5. **開始使用**

   * 在手機瀏覽器打開對應的 `.github.dev` 網址

---

## 📂 檔案規範

* **儲存路徑**：`/docs`
* **命名規則**：`YYYYMMDD_HHMM_自定義名稱.html`
* **靜態首頁**：

  ```
  https://jimmy0800.github.io/my-html-share/
  ```

---

## ⚠️ 注意事項

* 發布後請等待 GitHub Pages 部署完成（1～3 分鐘）
* 可至 GitHub 的 **Actions** 頁面確認部署狀態
* 確保 Codespaces 具備 Git 推送權限

---

## ⚡ 快速預覽（不等部署）

若只想先確認畫面是否正確：

1. 在 Codespaces 側邊欄打開 `docs` 資料夾
2. 右鍵點擊 `.html` 檔案
3. 選擇 **Open Preview**

可立即看到結果，無需等待 GitHub Pages。


