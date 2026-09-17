// NuevaMente Landing Page Interactions
document.addEventListener('DOMContentLoaded', () => {
  // 1. Interactive 3D Flashcard Flip
  const flashcard = document.getElementById('hero-flashcard');
  if (flashcard) {
    flashcard.addEventListener('click', () => {
      flashcard.classList.toggle('is-flipped');
    });
    flashcard.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        flashcard.classList.toggle('is-flipped');
      }
    });
  }

  // 2. SM-2 Rating Bar Demo
  const sm2Buttons = document.querySelectorAll('.nm-sm2__btn');
  const sm2Feedback = document.getElementById('sm2-feedback');
  
  sm2Buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      sm2Buttons.forEach(b => b.classList.remove('is-picked'));
      btn.classList.add('is-picked');
      
      const q = parseInt(btn.dataset.q, 10);
      let text = '';
      if (q < 3) {
        text = `Calificación ${q}/5: Repetición requerida hoy (Intervalo I=1 día, Factor de Facilidad ajustado).`;
      } else if (q === 3) {
        text = `Calificación 3/5 (Dificultad media): Próximo repaso en 3 días (EF conservador).`;
      } else if (q === 4) {
        text = `Calificación 4/5 (Respuesta correcta): Próximo repaso en 6 días (EF incrementa).`;
      } else {
        text = `Calificación 5/5 (Dominio perfecto): Próximo repaso en 10 días (Consolidación mnemotécnica).`;
      }
      if (sm2Feedback) {
        sm2Feedback.textContent = text;
      }
    });
  });

  // 3. Quiz Options Interactive Evaluation
  const quizOpts = document.querySelectorAll('.quiz-demo .nm-opt');
  quizOpts.forEach(opt => {
    opt.addEventListener('click', () => {
      quizOpts.forEach(o => {
        o.classList.remove('is-correct', 'is-wrong');
      });
      if (opt.dataset.correct === "true") {
        opt.classList.add('is-correct');
      } else {
        opt.classList.add('is-wrong');
      }
    });
  });
});
