document.addEventListener("DOMContentLoaded", function () {
    const hamburgerBtn = document.querySelector(".hamburger-btn");
    const navMenu = document.querySelector(".menu");

    // 初回ロード時に適切な表示状態を設定
    function updateMenuDisplay() {
        if (window.innerWidth > 480) {
            navMenu.classList.remove("active"); // PCではメニューを常に表示
            navMenu.style.display = "flex";
        } else {
            navMenu.classList.remove("active");
            navMenu.style.display = "none"; // スマホでは非表示
        }
    }

    // ハンバーガーボタンのクリックでメニューを開閉
    hamburgerBtn.addEventListener("click", function () {
        if (window.innerWidth <= 480) {
            navMenu.classList.toggle("active");
            navMenu.style.display = navMenu.classList.contains("active") ? "block" : "none";
        }
    });

    // 画面サイズ変更時にメニューを適切に設定
    window.addEventListener("resize", updateMenuDisplay);

    // 初回ロード時のメニュー表示を設定
    updateMenuDisplay();
});
document.querySelectorAll('.result_btn').forEach(button => {
    button.addEventListener('click', () => {
      button.style.opacity = '0.7';
      setTimeout(() => {
        button.style.opacity = '1';
      }, 200);
    });
  });
