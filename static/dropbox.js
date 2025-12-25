const fileInput = document.getElementById('fileInput');
const dropArea = document.getElementById('dropArea');
const dropText = document.getElementById('dropText');
const fileNamesDiv = document.getElementById('fileNames');
let filesList = []; // 이 배열에 파일들이 저장됩니다.

// 드래그된 파일을 dropArea에 드롭했을 때
dropArea.addEventListener('dragover', (event) => {
  event.preventDefault(); // 기본 동작을 막고
  dropArea.classList.add('drag-over'); // 드래그 영역 스타일 추가
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('drag-over'); // 드래그가 영역을 벗어나면 스타일 제거
});

dropArea.addEventListener('drop', (event) => {
  event.preventDefault();
  dropArea.classList.remove('drag-over'); // 드래그가 끝나면 스타일 제거
  const files = event.dataTransfer.files; // 드래그된 파일들
  addFiles(files); // 파일 추가 함수 호출
});

// 파일 input을 클릭하여 파일을 선택했을 때
dropArea.addEventListener('click', () => {
  fileInput.click(); // 숨겨진 파일 선택창을 클릭
});

fileInput.addEventListener('change', (event) => {
  const files = event.target.files;
  addFiles(files); // 파일 추가 함수 호출
});

function addFiles(files) {
  // 현재 올려진 파일 목록을 갱신
  const newFiles = Array.from(files); // FileList를 배열로 변환

  // 새로운 파일 목록을 filesList 배열에 덧붙입니다
  filesList = [...filesList, ...newFiles];

  // 파일 이름을 표시하는 영역을 갱신
  displayFileNames();
}

function displayFileNames() {
  // 파일 목록이 하나라도 있으면 안내 텍스트 숨기기
  if (filesList.length > 0) {
    dropText.style.display = 'none';
  }

  // 기존에 표시된 파일 이름 목록을 지웁니다.
  fileNamesDiv.innerHTML = ''; 

  // 파일 목록을 갱신하고 새로운 파일들을 표시
  filesList.forEach((file, index) => {
    const fileDiv = document.createElement('div');
    fileDiv.classList.add('file-item');
    
    const fileName = document.createElement('span');
    fileName.textContent = file.name; // 파일 이름 설정
    fileName.classList.add('file-name'); // 파일 이름 클래스 추가

    const removeBtn = document.createElement('button');
    removeBtn.textContent = 'X'; // "제거" 대신 "X"로 변경
    removeBtn.classList.add('remove-btn');
    removeBtn.addEventListener('click', () => {
      // 파일 삭제 로직: 해당 파일을 파일 목록에서 제거
      filesList = filesList.filter((_, i) => i !== index); // 해당 파일 제거
      displayFileNames();
    });
    
    fileDiv.appendChild(fileName);
    fileDiv.appendChild(removeBtn);
    fileNamesDiv.appendChild(fileDiv); // 파일 이름을 드랍박스 안에 표시
  });
}