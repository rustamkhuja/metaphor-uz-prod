const translations = {
  ru: {
    pageTitle:'Metaphor — слова для важного разговора', eyebrow:'AI-помощник для человеческих разговоров',
    heroTitle:'Найдите слова, которые действительно можно отправить',
    heroSubtitle:'Опишите ситуацию, цель и тон. Metaphor подготовит сообщение без шаблонного пафоса и лишних выдумок.',
    modes:{write:'Написать',reply:'Ответить',improve:'Улучшить',tone_check:'Проверить тон'},
    relationshipLabel:'Кому вы пишете?', relationships:{partner:'Партнёру или супругу',friend:'Другу',parent:'Родителю или старшему',colleague:'Коллеге',client:'Клиенту',other:'Другому человеку'},
    goalLabel:'Чего хотите добиться?', goals:{apologize:'Извиниться',support:'Поддержать',thank:'Поблагодарить',reconcile:'Помириться',congratulate:'Поздравить',set_boundary:'Спокойно обозначить границу',explain:'Объяснить позицию'},
    sourceWrite:'Что произошло?', sourceOther:'Вставьте исходное сообщение или текст', placeholderWrite:'Например: мы резко поговорили вчера. Я хочу извиниться, но без лишнего пафоса.', placeholderOther:'Вставьте сообщение или свой черновик и укажите желаемый результат.',
    toneLabel:'Тон', tones:{warm:'Тёплый',calm:'Спокойный',firm:'Уверенный',formal:'Формальный',light:'Лёгкий',romantic:'Романтичный'},
    lengthLabel:'Длина', lengths:{short:'Коротко',medium:'Обычно',long:'Развёрнуто'},
    addressLabel:'Обращение', addresses:{auto:'Автоматически',informal:'На «ты»',formal:'На «вы»'},
    consent:'Я понимаю, что текст обрабатывается AI, и не буду вводить лишние конфиденциальные данные.', more:'Подробнее',
    submit:'Создать сообщение', creating:'Создаю…', fine:'Проверьте и адаптируйте текст перед отправкой. Metaphor не заменяет профессиональную помощь.',
    result:'Готовый вариант', copy:'Скопировать', share:'Поделиться', shorter:'Короче', warmer:'Теплее', firmer:'Увереннее', fit:'Подошло?', yes:'Да', no:'Нет', privacy:'Конфиденциальность', terms:'Условия',
    limit:'Дневной бесплатный лимит исчерпан.'
  },
  uz: {
    pageTitle:'Metaphor — muhim suhbat uchun kerakli so‘zlar', eyebrow:'Insoniy suhbatlar uchun AI-yordamchi',
    heroTitle:'Haqiqatan ham yuborish mumkin bo‘lgan so‘zlarni toping',
    heroSubtitle:'Vaziyat, maqsad va ohangni yozing. Metaphor ortiqcha balandparvozliksiz tabiiy xabar tayyorlaydi.',
    modes:{write:'Yozish',reply:'Javob berish',improve:'Yaxshilash',tone_check:'Ohangni tekshirish'},
    relationshipLabel:'Kimga yozyapsiz?', relationships:{partner:'Turmush o‘rtoq yoki yaqin inson',friend:'Do‘st',parent:'Ota-ona yoki katta yoshli inson',colleague:'Hamkasb',client:'Mijoz',other:'Boshqa inson'},
    goalLabel:'Nimaga erishmoqchisiz?', goals:{apologize:'Uzr so‘rash',support:'Qo‘llab-quvvatlash',thank:'Minnatdorchilik bildirish',reconcile:'Yarashish',congratulate:'Tabriklash',set_boundary:'Chegarani xotirjam belgilash',explain:'Fikrni tushuntirish'},
    sourceWrite:'Nima bo‘ldi?', sourceOther:'Asl xabar yoki matningizni kiriting', placeholderWrite:'Masalan: kecha qattiq gaplashdik. Ortiqcha balandparvozliksiz uzr so‘ramoqchiman.', placeholderOther:'Xabarni yoki qoralamangizni kiriting va qanday natija kerakligini ko‘rsating.',
    toneLabel:'Ohang', tones:{warm:'Iliq',calm:'Xotirjam',firm:'Qat’iy',formal:'Rasmiy',light:'Yengil',romantic:'Romantik'},
    lengthLabel:'Uzunligi', lengths:{short:'Qisqa',medium:'O‘rtacha',long:'Batafsil'},
    addressLabel:'Murojaat', addresses:{auto:'Avtomatik',informal:'Sen shakli',formal:'Siz shakli'},
    consent:'Matn AI orqali qayta ishlanishini tushunaman va ortiqcha maxfiy ma’lumot kiritmayman.', more:'Batafsil',
    submit:'Xabar yaratish', creating:'Yaratilmoqda…', fine:'Yuborishdan oldin matnni tekshiring va moslashtiring. Metaphor professional yordam o‘rnini bosmaydi.',
    result:'Tayyor variant', copy:'Nusxalash', share:'Ulashish', shorter:'Qisqaroq', warmer:'Iliqroq', firmer:'Qat’iyroq', fit:'Mos keldimi?', yes:'Ha', no:'Yo‘q', privacy:'Maxfiylik', terms:'Shartlar'
  },
  en: {
    pageTitle:'Metaphor — words for an important conversation', eyebrow:'AI assistance for human conversations',
    heroTitle:'Find words you can actually send',
    heroSubtitle:'Describe the situation, goal and tone. Metaphor will prepare a natural message without invented details or generic drama.',
    modes:{write:'Write',reply:'Reply',improve:'Improve',tone_check:'Check tone'},
    relationshipLabel:'Who are you writing to?', relationships:{partner:'Partner or spouse',friend:'Friend',parent:'Parent or elder',colleague:'Colleague',client:'Client',other:'Someone else'},
    goalLabel:'What do you want to achieve?', goals:{apologize:'Apologize',support:'Offer support',thank:'Thank them',reconcile:'Reconcile',congratulate:'Congratulate',set_boundary:'Set a calm boundary',explain:'Explain your position'},
    sourceWrite:'What happened?', sourceOther:'Paste the original message or your draft', placeholderWrite:'For example: we spoke harshly yesterday. I want to apologize without sounding dramatic.', placeholderOther:'Paste the message or your draft and describe the outcome you want.',
    toneLabel:'Tone', tones:{warm:'Warm',calm:'Calm',firm:'Firm',formal:'Formal',light:'Light',romantic:'Romantic'},
    lengthLabel:'Length', lengths:{short:'Short',medium:'Normal',long:'Detailed'},
    addressLabel:'Form of address', addresses:{auto:'Automatic',informal:'Informal',formal:'Respectful/formal'},
    consent:'I understand that AI processes the text and I will not enter unnecessary confidential data.', more:'Learn more',
    submit:'Create message', creating:'Creating…', fine:'Review and adapt the text before sending. Metaphor does not replace professional support.',
    result:'Ready version', copy:'Copy', share:'Share', shorter:'Shorter', warmer:'Warmer', firmer:'Firmer', fit:'Does it work?', yes:'Yes', no:'No', privacy:'Privacy', terms:'Terms'
  }
};

const form = document.getElementById('form');
const result = document.getElementById('result');
const variantsNode = document.getElementById('variants');
const modelNode = document.getElementById('model');
const submit = document.getElementById('submit-button');
let currentMode = 'write';
let currentGenerationId = null;
let selectedText = '';
let currentLang = localStorage.getItem('metaphor_language') || 'ru';

if (window.Telegram?.WebApp) { window.Telegram.WebApp.ready(); window.Telegram.WebApp.expand(); }

function setOptionLabels(name, values){
  document.querySelectorAll(`select[name="${name}"] option`).forEach(o=>{ if(values[o.value]) o.textContent=values[o.value]; });
}
function applyLanguage(lang){
  currentLang=translations[lang]?lang:'ru'; localStorage.setItem('metaphor_language',currentLang); document.documentElement.lang=currentLang;
  document.getElementById('lang').value=currentLang; const t=translations[currentLang]; document.title=t.pageTitle;
  document.getElementById('eyebrow').textContent=t.eyebrow; document.getElementById('hero-title').textContent=t.heroTitle; document.getElementById('hero-subtitle').textContent=t.heroSubtitle;
  document.querySelectorAll('.mode').forEach(b=>b.textContent=t.modes[b.dataset.mode]);
  document.getElementById('relationship-label').textContent=t.relationshipLabel; setOptionLabels('relationship',t.relationships);
  document.getElementById('goal-label').textContent=t.goalLabel; setOptionLabels('goal',t.goals);
  document.getElementById('tone-label').textContent=t.toneLabel; setOptionLabels('tone',t.tones);
  document.getElementById('length-label').textContent=t.lengthLabel; setOptionLabels('length',t.lengths);
  document.getElementById('address-label').textContent=t.addressLabel; setOptionLabels('address_form',t.addresses);
  document.getElementById('consent-text').textContent=t.consent; document.getElementById('privacy-more').textContent=t.more;
  submit.textContent=t.submit; document.getElementById('fine-text').textContent=t.fine; document.getElementById('result-title').textContent=t.result;
  document.getElementById('copy').textContent=t.copy; document.getElementById('share').textContent=t.share;
  document.querySelector('[data-refine="shorter"]').textContent=t.shorter; document.querySelector('[data-refine="warmer"]').textContent=t.warmer; document.querySelector('[data-refine="firmer"]').textContent=t.firmer;
  document.getElementById('fit-label').textContent=t.fit; document.getElementById('yes-button').textContent=t.yes; document.getElementById('no-button').textContent=t.no;
  document.getElementById('privacy-link').textContent=t.privacy; document.getElementById('terms-link').textContent=t.terms;
  updateSourceLabel();
}
function updateSourceLabel(){ const t=translations[currentLang]; document.getElementById('source-label-text').textContent=currentMode==='write'?t.sourceWrite:t.sourceOther; form.elements.context.placeholder=currentMode==='write'?t.placeholderWrite:t.placeholderOther; }

document.getElementById('lang').addEventListener('change',e=>applyLanguage(e.target.value));
document.querySelectorAll('.mode').forEach(btn => btn.addEventListener('click', () => { document.querySelectorAll('.mode').forEach(x => x.classList.remove('active')); btn.classList.add('active'); currentMode = btn.dataset.mode; updateSourceLabel(); }));

function render(data) {
  currentGenerationId = data.generation_id; variantsNode.innerHTML = '';
  data.variants.forEach((v, i) => { const node=document.createElement('div'); node.className='variant'; node.contentEditable='true'; node.dataset.index=i; node.textContent=v.text; node.addEventListener('focus',()=>selectedText=node.innerText.trim()); node.addEventListener('input',()=>selectedText=node.innerText.trim()); variantsNode.appendChild(node); });
  selectedText = data.variants[0]?.text || ''; modelNode.textContent = `${data.provider} · ${data.model}`; result.classList.remove('hidden'); result.scrollIntoView({behavior:'smooth',block:'start'});
}

form.addEventListener('submit', async (e) => {
  e.preventDefault(); submit.disabled=true; submit.textContent=translations[currentLang].creating; variantsNode.innerHTML='';
  try {
    const fd=new FormData(form); const context=fd.get('context')||'';
    const payload={mode:currentMode,language:currentLang,relationship:fd.get('relationship'),goal:fd.get('goal'),tone:fd.get('tone'),output_format:'message',length:fd.get('length'),context:currentMode==='write'?context:'',source_text:currentMode==='write'?'':context,recipient_name:'',address_form:fd.get('address_form'),source:'web',partner_code:'',tier:'free',accepted_terms:fd.get('accepted_terms')==='on'};
    const response=await fetch('/api/v1/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); const data=await response.json(); if(!response.ok) throw new Error(data.detail||'Error'); render(data);
  } catch(err){ result.classList.remove('hidden'); variantsNode.innerHTML='<div class="error"></div>'; variantsNode.querySelector('.error').textContent=err.message; }
  finally { submit.disabled=false; submit.textContent=translations[currentLang].submit; }
});

document.getElementById('copy').addEventListener('click', async () => { await navigator.clipboard.writeText(selectedText); await sendFeedback(0,true,'copied'); });
document.getElementById('share').addEventListener('click', async () => { if(navigator.share) await navigator.share({text:selectedText}); else await navigator.clipboard.writeText(selectedText); await sendFeedback(0,true,'shared'); });
document.querySelectorAll('.refine').forEach(btn=>btn.addEventListener('click',async()=>{ if(!currentGenerationId||!selectedText)return; const response=await fetch(`/api/v1/generate/${currentGenerationId}/refine`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({instruction:btn.dataset.refine,selected_text:selectedText})}); const data=await response.json(); if(response.ok)render(data);else alert(data.detail||'Error'); }));
document.querySelectorAll('[data-rating]').forEach(btn=>btn.addEventListener('click',()=>sendFeedback(Number(btn.dataset.rating),false,'explicit')));
async function sendFeedback(rating,sentOrCopied,reason){ if(!currentGenerationId)return; await fetch('/api/v1/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({generation_id:currentGenerationId,rating,reason,comment:'',sent_or_copied:sentOrCopied})}); }

applyLanguage(currentLang);
