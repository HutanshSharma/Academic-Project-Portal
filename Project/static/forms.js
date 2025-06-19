let skills=[];


const slider = document.getElementById('page-score');
const scoreOutput = document.getElementById('score-output');


if (slider && scoreOutput) {
    scoreOutput.textContent = slider.value/10;

    slider.addEventListener('input', function () {
        scoreOutput.textContent = this.value/10;
        scoreOutput.classList.add('updated');
        setTimeout(() => {
            scoreOutput.classList.remove('updated');
        }, 500);
    });
}


if(document.getElementById("update")){
  console.log("print")
  addSkillsToDisplay()
}


function addSkillsToDisplay(){
  const input=document.getElementById("skills");
  const skillsstr=input.value.trim();
  const skillarr=skillsstr.split(",")
  for(let i=0;i<skillarr.length;i++){
    if(skillarr[i] && !skills.includes(skillarr[i])){
      skills.push(skillarr[i].trim());
      input.value="";
    }
  }
  updateDisplay();
}


const inputtaken=document.getElementById("skillInput");

inputtaken.addEventListener("keydown",function(event) {
  if(event.key==="Enter") {
    event.preventDefault();
    addSkill();
  }
});


function addSkill() {
    const input=document.getElementById("skillInput");
    const skill=input.value.trim();
    if(skill && !skills.includes(skill)) {
        skills.push(skill);
        input.value="";
        updateDisplay();
    }
  }


function updateDisplay() {
  const container=document.getElementById("skillsDisplay");
  container.innerHTML="";

  skills.forEach((skill,i) => {
      const tag=document.createElement("span");
      tag.textContent=skill + " ";

      tag.style.background="#111827"
      tag.style.margin="0 0.5rem 0 0"
      tag.style.padding="0.5rem 0.25rem 0.5rem 0.75rem";
      tag.style.border="solid 0.09rem #black";
      tag.style.borderRadius="10px";

    const remove=document.createElement("button");
    remove.innerHTML="×";
    remove.onclick=() => {
          skills.splice(i, 1);
          updateDisplay();
    };

      remove.style.color = "white";
      remove.style.background = "#6b020e";
      remove.style.marginLeft = "0.5rem";
      remove.style.height = "1.75rem";
      remove.style.width = "1.75rem";
      remove.style.border = "solid 0.025rem black";
      remove.style.borderRadius = "0.25rem";
      remove.style.cursor = "pointer";

      tag.appendChild(remove);
      container.appendChild(tag);
  });

  document.getElementById("skills").value =skills.join(", ");
}


document.getElementById("image").addEventListener("change", function() {
    const fileName=document.getElementById("file-name");
    const file=this.files[0];
    if(file){
      fileName.textContent=file.name;
    }
    else{
      fileName.textContent="No file chosen"
    }
});




