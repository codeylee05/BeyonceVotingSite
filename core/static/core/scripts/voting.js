document.addEventListener('DOMContentLoaded', () => {
    const voteButtons = document.querySelectorAll('.vote-btn');

    voteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const albumId = button.dataset.albumId;

            fetch(`/vote/${albumId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json'
                },
            })
                .then(resp => resp.json())
                .then(data => {
                    showAlert(data.message, data.success ? 'success' : 'warning');
                })
                .catch(err => {
                    console.error(err);
                    showAlert('Something went wrong. Please try again.', 'danger');
                });
        });
    });

    // ------------------------
    // CSRF helper
    // ------------------------
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ------------------------
    // Bootstrap Alert helper
    // ------------------------
    function showAlert(message, type = 'info') {
        const container = document.getElementById('alert-container');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        container.appendChild(alert);

        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 8000);
    }
});
