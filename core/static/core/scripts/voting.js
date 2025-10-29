document.addEventListener('DOMContentLoaded', () => {
    const voteButtons = document.querySelectorAll('.vote-btn');

    voteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const voteUrl = button.dataset.voteUrl; // use template-provided URL

            fetch(voteUrl, {
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
        if (!container) return; // avoid errors if container missing

        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        container.prepend(alert); // prepend to show above everything

        // Auto-dismiss after 8 seconds
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 8000);
    }
});
