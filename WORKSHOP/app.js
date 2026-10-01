/* Motor do site do workshop. Lê window.WORKSHOP, GERADO por LOOPS/WORKSHOP/montar.py a partir dos .md.
   Nada de conteúdo mora aqui: para mudar o texto, edite o .md e rode o montar.py de novo. */
(function () {
  "use strict";
  var W = window.WORKSHOP;
  var main = document.getElementById("conteudo");
  if (!W) {
    main.innerHTML = "<p>Falta o <code>conteudo.js</code>. Rode <code>python LOOPS/WORKSHOP/montar.py MISSOES/&lt;id&gt;</code>.</p>";
    return;
  }

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function slug(t) { return String(t).trim().toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu, "").replace(/\s/g, "-"); }
  function semAcento(s) { return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  function inline(md) { return window.marked && marked.parseInline ? marked.parseInline(md || "") : esc(md); }
  function textoPuro(md) { return String(md || "").replace(/\[([^\]]+)\]\([^)]*\)/g, "$1").replace(/[*`_]/g, ""); }

  /* progresso e preferências no navegador; pode faltar (janela anônima, bloqueio) e o site funciona sem */
  var CHAVE = "workshop-antigravity:v1";
  var EST = (function () { try { return JSON.parse(localStorage.getItem(CHAVE)) || {}; } catch (e) { return {}; } })();
  EST.ck = EST.ck || {}; EST.feito = EST.feito || {};
  function salvar() { try { localStorage.setItem(CHAVE, JSON.stringify(EST)); } catch (e) { /* sem armazenamento */ } }

  var PAG = {}, GL = {}, FT = {};
  W.paginas.forEach(function (p) { PAG[p.id] = p; });
  W.glossario.forEach(function (t) { GL[t.id] = t; });
  W.fontes.forEach(function (f) { FT[f.id] = f; });
  var ORDEM = W.paginas.filter(function (p) { return p.id !== "glossario"; });
  var DIAS = W.paginas.filter(function (p) { return p.meta && p.meta.agenda; });
  var TIPO = { conversa: "🗣️ conversa", demo: "🎬 demo", lab: "🧪 lab", checkpoint: "✅ checkpoint", tour: "🧭 tour" };
  var atual = null, JSONS = [], RAIZES = [], CRONS = [];

  /* ---------------------------------------------------------------- Markdown → DOM */
  function paraDom(md) {
    md = md.replace(/^```json jsoncrack[ \t]*$/gm, "```jsoncrack");
    var d = document.createElement("div");
    d.className = "md";
    if (window.marked && marked.parse) d.innerHTML = marked.parse(md, { gfm: true });
    else d.innerHTML = '<p class="aviso-cdn">O leitor de Markdown (marked, CDN jsDelivr) não carregou: sem internet, o texto aparece cru.</p><pre>' + esc(md) + "</pre>";
    return d;
  }

  function idsNosTitulos(raiz) {
    var vistos = {};
    $$("h1,h2,h3,h4", raiz).forEach(function (h) {
      var s = slug(h.textContent), n = vistos[s] || 0;
      vistos[s] = n + 1;
      if (!h.id) h.id = n ? s + "-" + n : s;
    });
  }

  function ancoraDe(n) {
    if (n.nodeType !== 1) return null;
    if (n.tagName === "A" && n.id) return n.id;
    if (n.tagName === "P" && n.children.length === 1 && n.firstElementChild.tagName === "A" && n.firstElementChild.id && !n.textContent.trim()) return n.firstElementChild.id;
    return null;
  }

  function blocos(raiz, pag) {
    var porId = {};
    ((pag.meta && pag.meta.agenda) || []).forEach(function (b) { porId[b.id] = b; });
    var sec = null;
    Array.prototype.slice.call(raiz.childNodes).forEach(function (n) {
      var a = ancoraDe(n);
      if (a && porId[a]) {
        sec = document.createElement("section");
        sec.className = "bloco" + (porId[a].parte === "extensao" ? " ext" : "");
        sec.setAttribute("data-bloco", a);
        raiz.insertBefore(sec, n);
      }
      if (sec) sec.appendChild(n);
    });
    $$("section.bloco", raiz).forEach(function (s) {
      var b = porId[s.getAttribute("data-bloco")], h = s.querySelector("h2");
      if (!h) return;
      var chave = pag.id + "|" + b.id, f = document.createElement("span");
      f.className = "ferr";
      f.innerHTML = '<span class="tipo">' + (TIPO[b.tipo] || b.tipo) + (b.parte === "extensao" ? " · extensão" : "") + "</span>" +
        '<button class="btn cron" type="button" title="Cronômetro do bloco (clique: iniciar/pausar · duplo clique: zerar)">⏱️ ' + b.min + ":00</button>" +
        '<button class="btn feito-btn" type="button" title="Marcar o bloco como feito">✓ feito</button>';
      h.appendChild(f);
      var fb = $(".feito-btn", f);
      fb.classList.toggle("on", !!EST.feito[chave]);
      fb.addEventListener("click", function () {
        if (EST.feito[chave]) delete EST.feito[chave]; else EST.feito[chave] = true;
        fb.classList.toggle("on", !!EST.feito[chave]);
        salvar(); desenharLateral(atual); marcarAgenda();
      });
      ligarCron($(".cron", f), b.min);
    });
  }

  function ligarCron(b, min) {
    var total = min * 60, resta = total, id = null;
    function mostra() {
      var a = Math.abs(resta), m = Math.floor(a / 60), s = a % 60;
      b.textContent = "⏱️ " + (resta < 0 ? "−" : "") + m + ":" + (s < 10 ? "0" : "") + s;
      b.classList.toggle("fim", resta <= 0);
    }
    function parar() { if (id) { clearInterval(id); id = null; } b.classList.remove("rodando"); }
    b.addEventListener("click", function () {
      if (id) { parar(); return; }
      CRONS.forEach(function (c) { c(); });
      id = setInterval(function () { resta -= 1; mostra(); }, 1000);
      b.classList.add("rodando");
    });
    b.addEventListener("dblclick", function () { parar(); resta = total; mostra(); });
    CRONS.push(parar);
  }

  var ALERTA = { TIP: ["tip", "💡 Dica"], NOTE: ["note", "🔎 Por baixo"], IMPORTANT: ["important", "🏢 No nosso trabalho"],
    WARNING: ["warning", "⚠️ Cuidado"], CAUTION: ["caution", "🔴 Segurança e custo"] };
  function cards(raiz) {
    $$("blockquote", raiz).forEach(function (bq) {
      var p = bq.firstElementChild;
      if (!p) return;
      var m = p.innerHTML.match(/^\s*\[!(TIP|NOTE|IMPORTANT|WARNING|CAUTION)\]\s*(<br>)?\s*/);
      if (m) {
        var a = ALERTA[m[1]];
        p.innerHTML = p.innerHTML.slice(m[0].length);
        if (!p.textContent.trim() && !p.children.length) p.remove();
        bq.className = "card " + a[0];
        bq.insertAdjacentHTML("afterbegin", '<span class="rot">' + a[1] + "</span>");
      } else if (/^\s*🎙️/.test(p.textContent)) {
        bq.className = "facilitador";
      }
    });
  }

  function trilhas(raiz) {
    $$("h3", raiz).forEach(function (h) {
      var t = h.textContent.trim(), cor = t.indexOf("🟢") === 0 ? "verde" : t.indexOf("🔴") === 0 ? "vermelha" : null;
      if (!cor) return;
      var box = document.createElement("div");
      box.className = "trilha " + cor;
      h.parentNode.insertBefore(box, h);
      var n = h;
      while (n) {
        var prox = n.nextSibling;
        box.appendChild(n);
        n = prox;
        if (n && n.nodeType === 1 && (/^H[1-3]$/.test(n.tagName) || n.tagName === "HR" || n.tagName === "BLOCKQUOTE")) break;
      }
    });
    $$(".trilha", raiz).forEach(function (t) {
      if (t.parentNode.classList.contains("trilhas")) return;
      var prox = t.nextElementSibling;
      if (prox && prox.classList.contains("trilha")) {
        var g = document.createElement("div");
        g.className = "trilhas";
        t.parentNode.insertBefore(g, t);
        g.appendChild(t); g.appendChild(prox);
      }
    });
    $$("p", raiz).forEach(function (p) { if (/^\s*✅/.test(p.textContent) && /Pronto quando/.test(p.textContent)) p.className = "pronto"; });
  }

  function tarefas(raiz, pagId) {
    $$('li > input[type="checkbox"], li > p > input[type="checkbox"]', raiz).forEach(function (cb) {
      var li = cb.closest("li"), chave = pagId + "|" + slug(li.textContent).slice(0, 80);
      cb.disabled = false;
      li.classList.add("tarefa");
      cb.checked = !!EST.ck[chave];
      li.classList.toggle("ok", cb.checked);
      cb.addEventListener("change", function () {
        if (cb.checked) EST.ck[chave] = true; else delete EST.ck[chave];
        li.classList.toggle("ok", cb.checked);
        salvar();
      });
    });
  }

  function codigos(raiz) {
    $$("pre > code", raiz).forEach(function (c) {
      var pre = c.parentNode, cls = c.className || "";
      if (/language-mermaid/.test(cls)) {
        var d = document.createElement("pre");
        d.className = "mermaid";
        d.textContent = c.textContent;
        pre.replaceWith(d);
        return;
      }
      if (/language-jsoncrack/.test(cls)) {
        var obj;
        try { obj = JSON.parse(c.textContent); } catch (e) { return; }
        var i = JSONS.push(obj) - 1, box = document.createElement("div");
        box.innerHTML = '<div class="jc" data-jc="' + i + '"><p class="carregando" style="padding:14px">o mapa carrega quando aparece na tela…</p></div>' +
          '<div class="jc-acoes"><button class="btn" type="button" data-jc-grande="' + i + '">🔍 abrir grande</button>' +
          "<details><summary>ver o JSON</summary><pre><code>" + esc(JSON.stringify(obj, null, 2)) + "</code></pre></details></div>";
        pre.replaceWith(box);
        return;
      }
      var b = document.createElement("button");
      b.className = "btn copiar"; b.type = "button"; b.textContent = "copiar";
      b.addEventListener("click", function () { copiar(c.textContent, b); });
      pre.appendChild(b);
    });
    $$("[data-jc-grande]", raiz).forEach(function (b) {
      b.addEventListener("click", function () { abrirModal("Mapa do JSON (JSONCrack)", JSONS[+b.getAttribute("data-jc-grande")]); });
    });
  }

  function copiar(txt, b) {
    function ok() { b.textContent = "copiado ✓"; setTimeout(function () { b.textContent = "copiar"; }, 1500); }
    function velho() {
      var t = document.createElement("textarea");
      t.value = txt; document.body.appendChild(t); t.select();
      try { document.execCommand("copy"); ok(); } catch (e) { /* sem área de transferência */ }
      t.remove();
    }
    try { navigator.clipboard.writeText(txt).then(ok, velho); } catch (e) { velho(); }
  }

  function links(raiz) {
    $$("a[href]", raiz).forEach(function (a) {
      var h = a.getAttribute("href"), m;
      if ((m = h.match(/^glossario\.md#(.+)$/))) {
        var id = decodeURIComponent(m[1]);
        a.classList.add("termo");
        a.setAttribute("href", "#/glossario/" + encodeURIComponent(id));
        a.addEventListener("click", function (e) { e.preventDefault(); abrirTermo(id); });
      } else if ((m = h.match(/^glossario\.md$/))) {
        a.setAttribute("href", "#/glossario");
      } else if ((m = h.match(/^(README|dia-\d+)\.md(?:#(.+))?$/))) {
        a.setAttribute("href", "#/p/" + m[1] + (m[2] ? "/" + m[2] : ""));
      } else if (/^https?:/.test(h)) {
        a.target = "_blank"; a.rel = "noopener";
      } else if (/^\.\.\/kit\//.test(h)) {
        a.target = "_blank"; a.title = "abre o arquivo do kit";
      }
    });
  }

  function selos(raiz) {
    var tw = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) { return /\[SRC-\d{2}\]/.test(n.nodeValue) && !n.parentNode.closest("code,pre") ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP; }
    });
    var nos = [];
    while (tw.nextNode()) nos.push(tw.currentNode);
    nos.forEach(function (n) {
      var s = document.createElement("span");
      s.innerHTML = esc(n.nodeValue).replace(/\[(SRC-\d{2})\]/g, function (_, id) {
        var f = FT[id] || { nome: "fonte não encontrada" };
        var dica = f.nome + (f.versao ? " · " + f.versao : "") + (f.lido_em ? " · lida em " + f.lido_em : "");
        return '<a class="fonte" href="#/fontes/' + id + '" title="' + esc(dica) + '">' + id + "</a>";
      });
      n.replaceWith.apply(n, Array.prototype.slice.call(s.childNodes));
    });
  }

  /* ---------------------------------------------------------------- JSONCrack e Mermaid (sob demanda) */
  var JC = null;
  function carregarJC() {
    if (JC) return JC;
    JC = Promise.all([
      import("https://esm.sh/react@18.3.1"),
      import("https://esm.sh/react-dom@18.3.1/client"),
      import("https://esm.sh/jsoncrack-react@1.0.5?deps=react@18.3.1,react-dom@18.3.1")
    ]).then(function (m) { return { React: m[0].default || m[0], createRoot: m[1].createRoot, JSONCrack: m[2].JSONCrack }; });
    return JC;
  }
  function renderJC(alvo, obj, extra) {
    alvo.innerHTML = '<p class="carregando" style="padding:14px">carregando o mapa…</p>';
    return carregarJC().then(function (jc) {
      alvo.innerHTML = "";
      var root = jc.createRoot(alvo);
      root.render(jc.React.createElement(jc.JSONCrack, Object.assign({ json: obj, theme: "dark", layoutDirection: "RIGHT", showControls: true, showGrid: true }, extra || {})));
      RAIZES.push(root);
      return root;
    }).catch(function () {
      alvo.innerHTML = '<p class="aviso-cdn" style="padding:14px">O JSONCrack não carregou (vem do CDN esm.sh e precisa de internet). Use "ver o JSON".</p>';
      return null;
    });
  }
  function ligarJC(raiz) {
    var caixas = $$(".jc[data-jc]", raiz);
    if (!caixas.length) return;
    if (!("IntersectionObserver" in window)) { caixas.forEach(function (c) { renderJC(c, JSONS[+c.getAttribute("data-jc")]); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); renderJC(e.target, JSONS[+e.target.getAttribute("data-jc")]); } });
    }, { rootMargin: "200px" });
    caixas.forEach(function (c) { io.observe(c); });
  }
  var modal = $("#modal"), raizModal = null;
  function abrirModal(tit, obj) {
    $("#mTit").textContent = tit;
    modal.hidden = false;
    var alvo = document.createElement("div");
    alvo.className = "jc";
    $("#mCorpo").innerHTML = "";
    $("#mCorpo").appendChild(alvo);
    renderJC(alvo, obj).then(function (r) { raizModal = r; });
  }
  function fecharModal() { if (raizModal) { raizModal.unmount(); raizModal = null; } modal.hidden = true; }
  $("#mFecha").onclick = fecharModal;
  modal.addEventListener("click", function (e) { if (e.target === modal) fecharModal(); });

  var MM = null;
  function carregarMM() {
    if (MM) return MM;
    MM = import("https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs").then(function (m) {
      var mm = m.default;
      mm.initialize({
        startOnLoad: false, securityLevel: "strict", theme: "base",
        themeVariables: {
          darkMode: true, background: "#181825", primaryColor: "#1e1e2e", primaryBorderColor: "#585b70", primaryTextColor: "#cdd6f4",
          secondaryColor: "#313244", tertiaryColor: "#181825", lineColor: "#7f849c", textColor: "#cdd6f4", mainBkg: "#1e1e2e",
          nodeBorder: "#585b70", clusterBkg: "#181825", clusterBorder: "#45475a", titleColor: "#a6adc8", edgeLabelBackground: "#181825",
          fontFamily: "Work Sans, system-ui, sans-serif", fontSize: "14px", actorBkg: "#1e1e2e", actorBorder: "#585b70",
          actorTextColor: "#cdd6f4", signalColor: "#a6adc8", signalTextColor: "#cdd6f4", noteBkgColor: "#313244",
          noteTextColor: "#cdd6f4", noteBorderColor: "#585b70", labelBoxBkgColor: "#1e1e2e", labelTextColor: "#cdd6f4",
          git0: "#89b4fa", git1: "#a6e3a1", git2: "#fab387", git3: "#cba6f7", gitBranchLabel0: "#11111b", gitBranchLabel1: "#11111b",
          commitLabelColor: "#cdd6f4", commitLabelBackground: "#313244"
        },
        flowchart: { curve: "basis", htmlLabels: true, padding: 12 }, sequence: { mirrorActors: false }
      });
      return mm;
    });
    return MM;
  }
  function rodarMermaid(raiz) {
    var nos = $$(".mermaid:not([data-processed])", raiz);
    if (!nos.length) return;
    carregarMM().then(function (mm) { return mm.run({ nodes: nos }); }).catch(function () {
      nos.forEach(function (n) { n.insertAdjacentHTML("afterend", '<p class="aviso-cdn">O diagrama não carregou (Mermaid vem do CDN jsDelivr e precisa de internet).</p>'); });
    });
  }

  /* ---------------------------------------------------------------- páginas */
  function soma(ag, parte) { return ag.filter(function (b) { return b.parte === parte; }).reduce(function (s, b) { return s + b.min; }, 0); }

  function cabecalhoDia(p) {
    var m = p.meta, ag = m.agenda, d = document.createElement("div");
    d.className = "cab-dia";
    d.innerHTML = '<p class="perg">❓ ' + esc(m.pergunta) + "</p>" +
      '<div class="meta"><span class="chip nuc">núcleo ' + soma(ag, "nucleo") + " min</span>" +
      '<span class="chip ext">extensão ' + soma(ag, "extensao") + " min</span>" +
      (m.precisa || []).map(function (x) { return '<span class="chip">📌 antes: ' + esc(x) + "</span>"; }).join("") + "</div>" +
      '<div class="agenda">' + ag.map(function (b) {
        return '<a href="#/p/' + p.id + "/" + b.id + '" data-bloco="' + b.id + '" class="' + (b.parte === "extensao" ? "ext " : "") + (b.tipo === "lab" ? "lab " : "") + (b.min < 6 ? "curto" : "") +
          '" style="--m:' + b.min + '" title="' + esc(b.min + " min · " + b.titulo) + '"><b>' + b.min + " min</b><span>" + esc(b.titulo) + "</span></a>";
      }).join("") + "</div>" +
      '<div class="leg">azul = núcleo · tracejado = extensão · verde = lab · clique num bloco para ir até ele</div>' +
      "<details><summary>🎯 Objetivos do encontro</summary><ul>" + (m.objetivos || []).map(function (o) { return "<li>" + inline(o) + "</li>"; }).join("") + "</ul></details>";
    return d;
  }
  function marcarAgenda() {
    $$(".agenda a[data-bloco]").forEach(function (a) { a.classList.toggle("feito", !!EST.feito[atual + "|" + a.getAttribute("data-bloco")]); });
  }
  function paraCasa(p) {
    var d = document.createElement("div");
    d.className = "md";
    d.innerHTML = '<div class="card important"><span class="rot">🏠 Para casa</span><ul>' +
      p.meta.para_casa.map(function (x) { return "<li>" + inline(x) + "</li>"; }).join("") + "</ul></div>";
    links(d); selos(d);
    return d;
  }
  function navegacao(p) {
    var i = ORDEM.indexOf(p), ant = ORDEM[i - 1], prox = ORDEM[i + 1], d = document.createElement("div");
    d.className = "nav-pag";
    d.innerHTML = (ant ? '<a class="btn" href="#/p/' + ant.id + '">← ' + esc(ant.titulo) + "</a>" : "<span></span>") +
      (prox ? '<a class="btn" href="#/p/' + prox.id + '">' + esc(prox.titulo) + " →</a>" : '<a class="btn" href="#/glossario">📖 Glossário →</a>');
    return d;
  }
  function limpar() {
    CRONS.forEach(function (c) { c(); }); CRONS = [];
    RAIZES.forEach(function (r) { try { r.unmount(); } catch (e) { /* já desmontado */ } }); RAIZES = [];
    JSONS = [];
    window.scrollTo(0, 0);
  }

  function verPagina(id, ancora) {
    var p = PAG[id];
    if (!p) { main.innerHTML = '<div class="pagina"><p>Página não encontrada. <a href="#/p/README">Voltar ao começo</a>.</p></div>'; return; }
    if (id === "glossario") { location.hash = "#/glossario"; return; }
    limpar();
    var dom = paraDom(p.md);
    idsNosTitulos(dom);
    if (p.meta && p.meta.agenda) blocos(dom, p);
    cards(dom); trilhas(dom); tarefas(dom, p.id); codigos(dom); links(dom); selos(dom);
    var art = document.createElement("article");
    art.className = "pagina";
    if (p.meta && p.meta.agenda) art.appendChild(cabecalhoDia(p));
    art.appendChild(dom);
    if (p.meta && p.meta.para_casa) art.appendChild(paraCasa(p));
    art.appendChild(navegacao(p));
    main.innerHTML = "";
    main.appendChild(art);
    marcarAgenda();
    ligarJC(art); rodarMermaid(art);
    desenharLateral(id);
    document.title = p.titulo + " · Workshop Antigravity";
    var alvo = ancora ? document.getElementById(ancora) : null;
    if (alvo) setTimeout(function () { alvo.scrollIntoView({ block: "start" }); window.scrollBy(0, -70); }, 30);
    else window.scrollTo(0, 0);
  }

  function htmlTermo(t) {
    return '<div class="g-termo"><h2>' + esc(t.termo) + "</h2>" +
      '<div class="g-camada s"><b>🟢 Simples</b>' + inline(t.simples) + "</div>" +
      '<div class="g-camada t"><b>🔴 Técnico</b>' + inline(t.tecnico) + "</div>" +
      (t.onde ? '<div class="g-camada w"><b>🧭 No workshop</b>' + inline(t.onde) + "</div>" : "") + "</div>";
  }
  function abrirTermo(id) {
    var t = GL[id];
    if (!t) return;
    var c = $("#gCorpo");
    c.innerHTML = htmlTermo(t) + '<p><a href="#/glossario/' + encodeURIComponent(id) + '">ver no glossário completo →</a></p>';
    links(c); selos(c);
    $("#gaveta").hidden = false;
  }
  $("#gFecha").onclick = function () { $("#gaveta").hidden = true; };

  function verGlossario(id) {
    limpar();
    main.innerHTML = '<div class="pagina md"><h1>📖 Glossário</h1><p>Cada termo tem duas leituras: <b>🟢 simples</b>, para quem está começando, e <b>🔴 técnica</b>, para quem já programa. Clique para abrir.</p>' +
      '<input id="filtro" type="search" placeholder="Filtrar termos…" aria-label="Filtrar termos"><div class="lista-gl"></div></div>';
    var lista = $(".lista-gl"), f = $("#filtro");
    function desenha() {
      var s = semAcento(f.value);
      lista.innerHTML = W.glossario.filter(function (t) { return !s || semAcento(t.termo + " " + t.simples + " " + t.tecnico).indexOf(s) >= 0; })
        .map(function (t) { return '<a href="#/glossario/' + encodeURIComponent(t.id) + '" data-t="' + esc(t.id) + '"><b>' + esc(t.termo) + "</b><small>" + esc(textoPuro(t.simples)) + "</small></a>"; }).join("");
      $$("a[data-t]", lista).forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); abrirTermo(a.getAttribute("data-t")); }); });
    }
    f.addEventListener("input", desenha);
    desenha();
    desenharLateral("glossario");
    document.title = "Glossário · Workshop Antigravity";
    if (id) abrirTermo(id);
  }

  function verFontes(id) {
    limpar();
    main.innerHTML = '<div class="pagina md"><h1>🔎 Fontes</h1><p>Todo comando, arquivo e limite citado no workshop aponta para uma destas fontes. Onde a doc online diverge da versão instalada, os labs seguem a instalada.</p>' +
      "<table><thead><tr><th>id</th><th>fonte</th><th>versão</th><th>lida em</th><th>limitação</th></tr></thead><tbody>" +
      W.fontes.map(function (f) {
        return '<tr id="' + f.id + '"' + (f.id === id ? ' style="outline:2px solid var(--teal)"' : "") + "><td><code>" + f.id + "</code></td><td>" +
          (f.url ? '<a href="' + esc(f.url) + '" target="_blank" rel="noopener">' + esc(f.nome) + "</a>" : esc(f.nome)) + "</td><td>" + esc(f.versao || "") +
          "</td><td>" + esc(f.lido_em || "") + "</td><td>" + esc(f.limitacoes || "") + "</td></tr>";
      }).join("") + "</tbody></table></div>";
    desenharLateral("fontes");
    document.title = "Fontes · Workshop Antigravity";
    var alvo = id && document.getElementById(id);
    if (alvo) alvo.scrollIntoView({ block: "center" });
  }

  function verKit() {
    limpar();
    var grupos = {};
    W.kit.forEach(function (k) {
      var p = k.split("/"), g = p[1] === "gabarito" && p.length > 3 ? "gabarito/" + p[2] : p.length > 2 ? p[1] : "raiz do kit";
      (grupos[g] = grupos[g] || []).push(k);
    });
    var nomes = { inicial: "🟢 inicial/: o workspace que cada dupla copia", "caca-ao-risco": "🔴 caca-ao-risco/: o workspace do Lab 6 (não rode nada)", "raiz do kit": "🧰 raiz do kit" };
    main.innerHTML = '<div class="pagina md"><h1>🧰 Kit de labs</h1><p>Clique para abrir o arquivo. O passo a passo de cada lab está no encontro; a preparação está no <a href="#/p/README">Comece aqui</a>. ' +
      "O autoteste <code>python kit/testar.py</code> confere todos os labs sem rede, sem modelo e sem nuvem.</p>" +
      Object.keys(grupos).sort().map(function (g) {
        return '<div class="kit-grupo"><h3>' + esc(nomes[g] || "📁 " + g + "/: só o que o lab muda") + "</h3>" +
          grupos[g].map(function (k) { return '<a href="../' + esc(k) + '" target="_blank">' + esc(k.replace(/^kit\//, "")) + "</a>"; }).join("") + "</div>";
      }).join("") + "</div>";
    desenharLateral("kit");
    document.title = "Kit · Workshop Antigravity";
  }

  function verMapa() {
    limpar();
    main.innerHTML = '<div class="pagina md" style="max-width:none"><h1>🗺️ Mapa do workshop</h1>' +
      '<p class="leg">O workshop inteiro como grafo (JSONCrack). <b>Clique num nó que tem "abrir"</b> para ir até ele. Arraste para mover, role para aproximar.</p>' +
      '<div id="mapaTodo"></div></div>';
    renderJC($("#mapaTodo"), W.mapa, {
      onNodeClick: function (no) {
        var linha = (no.text || []).filter(function (t) { return t.key === "abrir"; })[0];
        if (linha && typeof linha.value === "string") location.hash = linha.value;
      }
    });
    desenharLateral("mapa");
    document.title = "Mapa · Workshop Antigravity";
  }

  /* ---------------------------------------------------------------- lateral, busca, rotas */
  function desenharLateral(ativa) {
    var h = '<nav class="lat"><a href="#/p/README" class="' + (ativa === "README" ? "ativa" : "") + '">🧭 Comece aqui</a>';
    DIAS.forEach(function (p) {
      var ag = p.meta.agenda, feitos = ag.filter(function (b) { return EST.feito[p.id + "|" + b.id]; }).length, pct = Math.round(100 * feitos / ag.length);
      h += '<div class="lat-dia"><h4><span>Dia ' + p.meta.dia + " · " + esc(p.titulo) + "</span><small>" + pct + "%</small></h4>" +
        '<div class="barra"><i style="width:' + pct + '%"></i></div>' +
        '<a href="#/p/' + p.id + '" class="' + (ativa === p.id ? "ativa" : "") + '">📅 abrir o encontro</a>' +
        ag.map(function (b) {
          var f = EST.feito[p.id + "|" + b.id];
          return '<a class="bl' + (b.parte === "extensao" ? " ext" : "") + (f ? " feito" : "") + '" href="#/p/' + p.id + "/" + b.id + '"><span class="ck">' + (f ? "✓" : "○") +
            '</span><span class="min">' + b.min + "′</span><span>" + esc(b.titulo) + "</span></a>";
        }).join("") + "</div>";
    });
    h += "<hr>" +
      '<a href="#/glossario" class="' + (ativa === "glossario" ? "ativa" : "") + '">📖 Glossário (' + W.glossario.length + " termos)</a>" +
      '<a href="#/kit" class="' + (ativa === "kit" ? "ativa" : "") + '">🧰 Kit de labs</a>' +
      '<a href="#/fontes" class="' + (ativa === "fontes" ? "ativa" : "") + '">🔎 Fontes (' + W.fontes.length + ")</a>" +
      '<a href="#/mapa" class="' + (ativa === "mapa" ? "ativa" : "") + '">🗺️ Mapa (JSONCrack)</a></nav>';
    $("#lateral").innerHTML = h;
  }

  var INDICE = null;
  function indice() {
    if (INDICE) return INDICE;
    INDICE = [];
    ORDEM.forEach(function (p) {
      p.md.split(/^(?=#{2,3} )/m).forEach(function (sec, i) {
        var tit = i === 0 ? p.titulo : sec.split("\n")[0].replace(/^#+\s*/, "");
        INDICE.push({ titulo: tit, onde: p.titulo, texto: semAcento(sec), href: "#/p/" + p.id + (i === 0 ? "" : "/" + slug(tit)) });
      });
    });
    W.glossario.forEach(function (t) {
      INDICE.push({ titulo: "📖 " + t.termo, onde: "glossário", texto: semAcento(t.termo + " " + t.simples + " " + t.tecnico), termo: t.id });
    });
    W.kit.forEach(function (k) { INDICE.push({ titulo: "🧰 " + k.split("/").pop(), onde: k, texto: semAcento(k), href: "../" + k, fora: true }); });
    return INDICE;
  }
  var q = $("#q"), qres = $("#qres"), sel = -1, achados = [];
  function buscar() {
    var s = semAcento(q.value.trim());
    if (s.length < 2) { qres.hidden = true; return; }
    achados = indice().map(function (it) { return { it: it, sc: (semAcento(it.titulo).indexOf(s) >= 0 ? 2 : 0) + (it.texto.indexOf(s) >= 0 ? 1 : 0) }; })
      .filter(function (x) { return x.sc; }).sort(function (a, b) { return b.sc - a.sc; }).slice(0, 12).map(function (x) { return x.it; });
    sel = achados.length ? 0 : -1;
    qres.innerHTML = achados.length ? achados.map(function (it, i) { return '<a href="#" data-i="' + i + '" class="' + (i === sel ? "sel" : "") + '">' + esc(it.titulo) + "<small>" + esc(it.onde) + "</small></a>"; }).join("")
      : '<a href="#" style="pointer-events:none">nada encontrado</a>';
    qres.hidden = false;
    $$("a[data-i]", qres).forEach(function (a) { a.addEventListener("mousedown", function (e) { e.preventDefault(); ir(achados[+a.getAttribute("data-i")]); }); });
  }
  function ir(it) {
    if (!it) return;
    qres.hidden = true; q.blur();
    if (it.termo) abrirTermo(it.termo);
    else if (it.fora) window.open(it.href, "_blank");
    else location.hash = it.href;
  }
  q.addEventListener("input", buscar);
  q.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      sel = Math.max(0, Math.min(achados.length - 1, sel + (e.key === "ArrowDown" ? 1 : -1)));
      $$("a[data-i]", qres).forEach(function (a, i) { a.classList.toggle("sel", i === sel); });
    } else if (e.key === "Enter") { e.preventDefault(); ir(achados[sel]); }
    else if (e.key === "Escape") { qres.hidden = true; q.blur(); }
  });
  q.addEventListener("blur", function () { setTimeout(function () { qres.hidden = true; }, 150); });
  document.addEventListener("keydown", function (e) {
    var digitando = /INPUT|TEXTAREA/.test((document.activeElement || {}).tagName || "");
    if (e.key === "/" && !digitando) { e.preventDefault(); q.focus(); }
    if (e.key === "Escape") { $("#gaveta").hidden = true; if (!modal.hidden) fecharModal(); document.body.classList.remove("menu"); }
  });

  var bF = $("#bFacil");
  function aplicarFacil() { document.body.classList.toggle("facil", !!EST.facil); bF.setAttribute("aria-pressed", EST.facil ? "true" : "false"); }
  bF.addEventListener("click", function () { EST.facil = !EST.facil; salvar(); aplicarFacil(); });
  $("#bMenu").addEventListener("click", function () { document.body.classList.toggle("menu"); });
  main.addEventListener("click", function () { document.body.classList.remove("menu"); });

  function rotear() {
    var h = location.hash.replace(/^#\/?/, ""), p = h.split("/").map(function (x) { try { return decodeURIComponent(x); } catch (e) { return x; } });
    document.body.classList.remove("menu");
    $("#gaveta").hidden = true;   // a gaveta do termo não segue a pessoa para outra página
    if (p[0] === "p" && p[1]) { atual = p[1]; verPagina(p[1], p.slice(2).join("/")); }
    else if (p[0] === "glossario") { atual = "glossario"; verGlossario(p[1]); }
    else if (p[0] === "fontes") { atual = "fontes"; verFontes(p[1]); }
    else if (p[0] === "kit") { atual = "kit"; verKit(); }
    else if (p[0] === "mapa") { atual = "mapa"; verMapa(); }
    else location.hash = "#/p/README";
  }
  window.addEventListener("hashchange", rotear);
  aplicarFacil();
  rotear();
  window.WS = { verPagina: verPagina, abrirTermo: abrirTermo, indice: indice };
})();
