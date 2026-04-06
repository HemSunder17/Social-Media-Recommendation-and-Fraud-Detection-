document.addEventListener('DOMContentLoaded', function () {

    // ── LIKE BUTTON ──────────────────────────────────────────
    document.querySelectorAll('.like-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const postId = this.dataset.postId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/posts/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(res => res.json())
            .then(data => {
                const icon = this.querySelector('i');
                const count = this.querySelector('span');
                if (data.liked) {
                    icon.classList.remove('fa-regular');
                    icon.classList.add('fa-solid');
                    this.classList.add('liked');
                } else {
                    icon.classList.remove('fa-solid');
                    icon.classList.add('fa-regular');
                    this.classList.remove('liked');
                }
                count.textContent = data.total_likes;
            });
        });
    });

    // ── TOGGLE COMMENTS ──────────────────────────────────────
    document.querySelectorAll('.toggle-comments-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const postId = this.dataset.postId;
            const section = document.getElementById(`comments-${postId}`);
            if (section.style.display === 'none' || section.style.display === '') {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    });

    // ── REPORT MODAL ─────────────────────────────────────────
    document.querySelectorAll('.report-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const postId = this.dataset.postId;
            const modal = document.getElementById('report-modal');
            const form = document.getElementById('report-form');
            form.action = `/fraud/report/${postId}/`;
            modal.classList.add('active');
        });
    });

    const modalOverlay = document.getElementById('report-modal');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function (e) {
            if (e.target === this) this.classList.remove('active');
        });
    }

    const cancelReport = document.getElementById('cancel-report');
    if (cancelReport) {
        cancelReport.addEventListener('click', function () {
            document.getElementById('report-modal').classList.remove('active');
        });
    }

    // ── AUTO HIDE ALERTS ─────────────────────────────────────
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // ── IMAGE PREVIEW ON CREATE POST ─────────────────────────
    const imageInput = document.getElementById('image-input');
    if (imageInput) {
        imageInput.addEventListener('change', function () {
            const preview = document.getElementById('image-preview');
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }

});