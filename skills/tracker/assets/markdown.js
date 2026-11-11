/* Markdown in a tracker's text: an item's context, what was found, the
   question, the plan, what was decided and done, and every reply. Shared by
   every tracker's page (inlined by `tracker.py build`) and by the Kata hub
   (served as-is). It builds DOM nodes and never parses HTML, so nothing written
   in a tracker can add markup or script to a page.

   The subset people and agents write in a note: paragraphs, where a single
   line break stays a line break; lists, bulleted or numbered, nested by
   indenting; headings (drawn at text size: a field's label is its heading);
   quotes; fenced code; pipe tables; a rule; and inline **bold**, *italic*,
   ~~struck~~, `code`, [links](…) and bare web addresses. A link goes to a web
   page or an email address only, in a new tab; any other keeps its words. A
   backslash keeps a marker literal. */
(function () {
  const el = (tag, attrs) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) n.setAttribute(k, v);
    return n;
  };

  // ------------------------------------------------------------ inline
  const INLINE = new RegExp([
    /\\([\\`*_{}\[\]()#+\-.!|~>])/,                              // 1 an escaped marker
    /(`+)([^`]|[^`][\s\S]*?[^`])\2(?!`)/,                         // 2, 3 code
    /\*\*(?=\S)([\s\S]*?\S)\*\*/,                                 // 4 bold
    /(?<![\w])__(?=\S)([\s\S]*?\S)__(?![\w])/,                    // 5 bold
    /\*(?=[^\s*])([\s\S]*?[^\s*])\*(?!\*)/,                       // 6 italic
    /(?<![\w])_(?=\S)([\s\S]*?\S)_(?![\w])/,                      // 7 italic
    /~~(?=\S)([\s\S]*?\S)~~/,                                     // 8 struck
    /\[((?:[^\[\]\\]|\\.)+)\]\(\s*<?([^\s<>()]+)>?(?:\s+"[^"]*")?\s*\)/, // 9, 10 a link
    /<((?:https?:\/\/|mailto:)[^\s<>]+)>/,                        // 11 an address in brackets
    /(https?:\/\/[^\s<>]*[^\s<>.,;:!?)\]'"*_~`])/,                // 12 a bare address
  ].map((r) => r.source).join("|"));
  const SAFE = /^(https?:\/\/|mailto:)/i;

  function link(href, kids) {
    if (!SAFE.test(href)) return kids;
    const a = el("a", { href, target: "_blank", rel: "noopener noreferrer" });
    a.append(...kids);
    return [a];
  }

  function inline(text) {
    const out = [];
    let rest = text;
    while (rest) {
      const m = INLINE.exec(rest);
      if (!m) { out.push(document.createTextNode(rest)); break; }
      if (m.index) out.push(document.createTextNode(rest.slice(0, m.index)));
      rest = rest.slice(m.index + m[0].length);
      const wrap = (tag, inner) => { const n = el(tag); n.append(...inline(inner)); return n; };
      if (m[1] !== undefined) out.push(document.createTextNode(m[1]));
      else if (m[3] !== undefined) { const c = el("code"); c.textContent = m[3].replace(/^ (.*) $/, "$1"); out.push(c); }
      else if (m[4] !== undefined || m[5] !== undefined) out.push(wrap("strong", m[4] !== undefined ? m[4] : m[5]));
      else if (m[6] !== undefined || m[7] !== undefined) out.push(wrap("em", m[6] !== undefined ? m[6] : m[7]));
      else if (m[8] !== undefined) out.push(wrap("s", m[8]));
      else if (m[9] !== undefined) out.push(...link(m[10], inline(m[9])));
      else { const href = m[11] !== undefined ? m[11] : m[12]; out.push(...link(href, [document.createTextNode(href)])); }
    }
    return out;
  }

  /* Lines of a paragraph, each line break kept. */
  function lines(into, list) {
    list.forEach((line, n) => {
      if (n) into.append(el("br"));
      into.append(...inline(line.trim()));
    });
    return into;
  }

  // ------------------------------------------------------------ blocks
  const ITEM = /^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$/;
  const FENCE = /^\s{0,3}(`{3,}|~{3,})\s*([\w+-]*)\s*$/;
  const HEADING = /^\s{0,3}#{1,6}\s+(.*?)(?:\s+#+)?\s*$/;
  const QUOTE = /^\s{0,3}>\s?(.*)$/;
  const RULE = /^\s{0,3}([-*_])(?:\s*\1){2,}\s*$/;
  const DIVIDER = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;
  const width = (s) => s.replace(/\t/g, "    ").length;
  const isTable = (src, i) => src[i].includes("|") && i + 1 < src.length && src[i + 1].includes("-") && DIVIDER.test(src[i + 1]);
  const starts = (src, i) => FENCE.test(src[i]) || HEADING.test(src[i]) || QUOTE.test(src[i]) || RULE.test(src[i]) || ITEM.test(src[i]) || isTable(src, i);

  function cells(line) {
    const s = line.trim().replace(/^\|/, "").replace(/(^|[^\\])\|$/, "$1");
    return s.split(/(?<!\\)\|/).map((c) => c.trim().replace(/\\\|/g, "|"));
  }

  function table(src, i, into) {
    const align = cells(src[i + 1]).map((c) => c.startsWith(":") && c.endsWith(":") ? "center" : c.endsWith(":") ? "right" : c.startsWith(":") ? "left" : "");
    const t = el("table"), row = (line, tag) => {
      const tr = el("tr");
      cells(line).forEach((c, n) => { const td = el(tag, align[n] ? { style: "text-align:" + align[n] } : {}); td.append(...inline(c)); tr.append(td); });
      return tr;
    };
    t.append(row(src[i], "th"));
    for (i += 2; i < src.length && src[i].trim() && src[i].includes("|"); i++) t.append(row(src[i], "td"));
    const wrap = el("div", { class: "tw" });
    wrap.append(t);
    into.append(wrap);
    return i;
  }

  /* A list from line `i`, and the items indented under each of its items. */
  function list(src, i, into) {
    const first = ITEM.exec(src[i]), base = width(first[1]), ordered = /\d/.test(first[2]);
    const ol = el(ordered ? "ol" : "ul");
    if (ordered && parseInt(first[2], 10) !== 1) ol.setAttribute("start", String(parseInt(first[2], 10)));
    let li = null;
    while (i < src.length) {
      if (!src[i].trim()) {                        // a blank line inside a list, when the list goes on
        let j = i; while (j < src.length && !src[j].trim()) j++;
        const m = j < src.length && ITEM.exec(src[j]);
        if (m && width(m[1]) >= base - 1) { i = j; continue; }
        if (li && j < src.length && width(src[j].match(/^\s*/)[0]) > base) { i = j; li.append(el("br")); continue; }
        break;
      }
      // An item one space off the list's indent is still its own; two or more in is nested.
      const m = ITEM.exec(src[i]), w = m ? width(m[1]) : 0;
      if (m && w > base + 1 && li) { i = list(src, i, li); continue; }
      if (m && w >= base - 1 && w <= base + 1) {
        if (/\d/.test(m[2]) !== ordered) break;    // the other kind of list starts a list of its own
        li = el("li");
        li.append(...inline(m[3].trim()));
        ol.append(li);
        i++;
        continue;
      }
      if (m) break;                                // a less indented item belongs to an outer list
      if (li && width(src[i].match(/^\s*/)[0]) > base && !starts(src, i)) {   // a line carried on under its item
        li.append(el("br"), ...inline(src[i].trim()));
        i++;
        continue;
      }
      break;
    }
    into.append(ol);
    return i;
  }

  function blocks(src, into) {
    let i = 0;
    while (i < src.length) {
      const line = src[i];
      if (!line.trim()) { i++; continue; }
      let m;
      if ((m = FENCE.exec(line))) {
        const close = new RegExp("^\\s{0,3}" + m[1][0] + "{" + m[1].length + ",}\\s*$"), body = [];
        for (i++; i < src.length && !close.test(src[i]); i++) body.push(src[i]);
        i++;
        const pre = el("pre"), code = el("code");
        code.textContent = body.join("\n");
        pre.append(code);
        into.append(pre);
      } else if ((m = HEADING.exec(line))) {
        const h = el("h4");
        h.append(...inline(m[1]));
        into.append(h);
        i++;
      } else if (RULE.test(line)) {
        into.append(el("hr"));
        i++;
      } else if (QUOTE.test(line)) {
        const inner = [];
        for (; i < src.length && (m = QUOTE.exec(src[i])); i++) inner.push(m[1]);
        const q = el("blockquote");
        blocks(inner, q);
        into.append(q);
      } else if (ITEM.test(line)) {
        i = list(src, i, into);
      } else if (isTable(src, i)) {
        i = table(src, i, into);
      } else {
        const para = [line];
        for (i++; i < src.length && src[i].trim() && !starts(src, i); i++) para.push(src[i]);
        into.append(lines(el("p"), para));
      }
    }
    return into;
  }

  /* The text as Markdown, in a block of class "md" (plus `cls`). */
  window.markdown = function (text, cls) {
    return blocks(String(text == null ? "" : text).replace(/\r\n?/g, "\n").split("\n"), el("div", { class: "md" + (cls ? " " + cls : "") }));
  };
})();
