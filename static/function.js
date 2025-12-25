document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.col-checkbox');
    const table = document.querySelector('table');
    
    
    // 변경위치 토글
    checkboxes.forEach((checkbox, index) => {
        checkbox.addEventListener('change', () => {
            document.querySelectorAll('table tr').forEach(row => {
                const cells = row.querySelectorAll('th, td');
                if (cells[index]) {
                    cells[index].style.display = checkbox.checked ? '' : 'none';
                }
            });
        });
    });
    

    // 다운로드
    const downloadForm = document.getElementById('downloadForm');
    if (downloadForm) {
        downloadForm.addEventListener('submit', e => {
            e.preventDefault();
    
            const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
            const visibleCols = Array.from(checkboxes)
                .map((cb, i) => cb.checked ? headers[i] : null)
                .filter(Boolean);
    
            const rows = Array.from(table.querySelectorAll('tbody tr')).filter(row => row.style.display !== 'none');
            const data = rows.map(row => {
                const cells = row.querySelectorAll('td');
                const rowData = {};
                visibleCols.forEach((col, i) => {
                    const colIndex = headers.indexOf(col);
                    rowData[col] = cells[colIndex] ? cells[colIndex].textContent.trim() : '';
                });
                return rowData;
            });
    
            document.getElementById('columnsInput').value = JSON.stringify(visibleCols);
            document.getElementById('dataInput').value = JSON.stringify(data);
    
            downloadForm.submit();
        });
    }
    });