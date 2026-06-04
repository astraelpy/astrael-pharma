// script.js
document.addEventListener('DOMContentLoaded', () => {
    // Confirmação para excluir itens
    const deleteBtns = document.querySelectorAll('.btn-delete');
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Tem certeza que deseja excluir este item? Essa ação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    });
});
