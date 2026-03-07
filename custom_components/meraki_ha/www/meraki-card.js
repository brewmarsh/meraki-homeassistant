/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ct = globalThis, Jt = Ct.ShadowRoot && (Ct.ShadyCSS === void 0 || Ct.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Wt = Symbol(), re = /* @__PURE__ */ new WeakMap();
let Ee = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== Wt) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Jt && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = re.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && re.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const Ve = (i) => new Ee(typeof i == "string" ? i : i + "", void 0, Wt), G = (i, ...t) => {
  const e = i.length === 1 ? i[0] : t.reduce((s, n, r) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(n) + i[r + 1], i[0]);
  return new Ee(e, i, Wt);
}, ze = (i, t) => {
  if (Jt) i.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), n = Ct.litNonce;
    n !== void 0 && s.setAttribute("nonce", n), s.textContent = e.cssText, i.appendChild(s);
  }
}, oe = Jt ? (i) => i : (i) => i instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return Ve(e);
})(i) : i;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: je, defineProperty: Ke, getOwnPropertyDescriptor: Ge, getOwnPropertyNames: qe, getOwnPropertySymbols: Je, getPrototypeOf: We } = Object, L = globalThis, ae = L.trustedTypes, Ye = ae ? ae.emptyScript : "", Rt = L.reactiveElementPolyfillSupport, rt = (i, t) => i, bt = { toAttribute(i, t) {
  switch (t) {
    case Boolean:
      i = i ? Ye : null;
      break;
    case Object:
    case Array:
      i = i == null ? i : JSON.stringify(i);
  }
  return i;
}, fromAttribute(i, t) {
  let e = i;
  switch (t) {
    case Boolean:
      e = i !== null;
      break;
    case Number:
      e = i === null ? null : Number(i);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(i);
      } catch {
        e = null;
      }
  }
  return e;
} }, Yt = (i, t) => !je(i, t), ce = { attribute: !0, type: String, converter: bt, reflect: !1, useDefault: !1, hasChanged: Yt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), L.litPropertyMetadata ?? (L.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let q = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = ce) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = Symbol(), n = this.getPropertyDescriptor(t, s, e);
      n !== void 0 && Ke(this.prototype, t, n);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: n, set: r } = Ge(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: n, set(o) {
      const c = n == null ? void 0 : n.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, c, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? ce;
  }
  static _$Ei() {
    if (this.hasOwnProperty(rt("elementProperties"))) return;
    const t = We(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(rt("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(rt("properties"))) {
      const e = this.properties, s = [...qe(e), ...Je(e)];
      for (const n of s) this.createProperty(n, e[n]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [s, n] of e) this.elementProperties.set(s, n);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, s] of this.elementProperties) {
      const n = this._$Eu(e, s);
      n !== void 0 && this._$Eh.set(n, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const s = new Set(t.flat(1 / 0).reverse());
      for (const n of s) e.unshift(oe(n));
    } else t !== void 0 && e.push(oe(t));
    return e;
  }
  static _$Eu(t, e) {
    const s = e.attribute;
    return s === !1 ? void 0 : typeof s == "string" ? s : typeof t == "string" ? t.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    var t;
    this._$ES = new Promise((e) => this.enableUpdating = e), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), (t = this.constructor.l) == null || t.forEach((e) => e(this));
  }
  addController(t) {
    var e;
    (this._$EO ?? (this._$EO = /* @__PURE__ */ new Set())).add(t), this.renderRoot !== void 0 && this.isConnected && ((e = t.hostConnected) == null || e.call(t));
  }
  removeController(t) {
    var e;
    (e = this._$EO) == null || e.delete(t);
  }
  _$E_() {
    const t = /* @__PURE__ */ new Map(), e = this.constructor.elementProperties;
    for (const s of e.keys()) this.hasOwnProperty(s) && (t.set(s, this[s]), delete this[s]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return ze(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    var t;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$EO) == null || t.forEach((e) => {
      var s;
      return (s = e.hostConnected) == null ? void 0 : s.call(e);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$EO) == null || t.forEach((e) => {
      var s;
      return (s = e.hostDisconnected) == null ? void 0 : s.call(e);
    });
  }
  attributeChangedCallback(t, e, s) {
    this._$AK(t, s);
  }
  _$ET(t, e) {
    var r;
    const s = this.constructor.elementProperties.get(t), n = this.constructor._$Eu(t, s);
    if (n !== void 0 && s.reflect === !0) {
      const o = (((r = s.converter) == null ? void 0 : r.toAttribute) !== void 0 ? s.converter : bt).toAttribute(e, s.type);
      this._$Em = t, o == null ? this.removeAttribute(n) : this.setAttribute(n, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const s = this.constructor, n = s._$Eh.get(t);
    if (n !== void 0 && this._$Em !== n) {
      const c = s.getPropertyOptions(n), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((r = c.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? c.converter : bt;
      this._$Em = n;
      const l = a.fromAttribute(e, c.type);
      this[n] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(n)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, n = !1, r) {
    var o;
    if (t !== void 0) {
      const c = this.constructor;
      if (n === !1 && (r = this[t]), s ?? (s = c.getPropertyOptions(t)), !((s.hasChanged ?? Yt)(r, e) || s.useDefault && s.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(c._$Eu(t, s)))) return;
      this.C(t, e, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: s, reflect: n, wrapped: r }, o) {
    s && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || s || (e = void 0), this._$AL.set(t, e)), n === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (e) {
      Promise.reject(e);
    }
    const t = this.scheduleUpdate();
    return t != null && await t, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    var s;
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this._$Ep) {
        for (const [r, o] of this._$Ep) this[r] = o;
        this._$Ep = void 0;
      }
      const n = this.constructor.elementProperties;
      if (n.size > 0) for (const [r, o] of n) {
        const { wrapped: c } = o, a = this[r];
        c !== !0 || this._$AL.has(r) || a === void 0 || this.C(r, void 0, o, a);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (s = this._$EO) == null || s.forEach((n) => {
        var r;
        return (r = n.hostUpdate) == null ? void 0 : r.call(n);
      }), this.update(e)) : this._$EM();
    } catch (n) {
      throw t = !1, this._$EM(), n;
    }
    t && this._$AE(e);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var e;
    (e = this._$EO) == null || e.forEach((s) => {
      var n;
      return (n = s.hostUpdated) == null ? void 0 : n.call(s);
    }), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(t)), this.updated(t);
  }
  _$EM() {
    this._$AL = /* @__PURE__ */ new Map(), this.isUpdatePending = !1;
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$ES;
  }
  shouldUpdate(t) {
    return !0;
  }
  update(t) {
    this._$Eq && (this._$Eq = this._$Eq.forEach((e) => this._$ET(e, this[e]))), this._$EM();
  }
  updated(t) {
  }
  firstUpdated(t) {
  }
};
q.elementStyles = [], q.shadowRootOptions = { mode: "open" }, q[rt("elementProperties")] = /* @__PURE__ */ new Map(), q[rt("finalized")] = /* @__PURE__ */ new Map(), Rt == null || Rt({ ReactiveElement: q }), (L.reactiveElementVersions ?? (L.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ot = globalThis, le = (i) => i, At = ot.trustedTypes, he = At ? At.createPolicy("lit-html", { createHTML: (i) => i }) : void 0, Ce = "$lit$", x = `lit$${Math.random().toFixed(9).slice(2)}$`, be = "?" + x, Qe = `<${be}>`, j = document, ct = () => j.createComment(""), lt = (i) => i === null || typeof i != "object" && typeof i != "function", Qt = Array.isArray, Ze = (i) => Qt(i) || typeof (i == null ? void 0 : i[Symbol.iterator]) == "function", Dt = `[
\f\r]`, st = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, ue = /-->/g, de = />/g, F = RegExp(`>|${Dt}(?:([^\\s"'>=/]+)(${Dt}*=${Dt}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), fe = /'/g, ge = /"/g, Ae = /^(?:script|style|textarea|title)$/i, Xe = (i) => (t, ...e) => ({ _$litType$: i, strings: t, values: e }), E = Xe(1), J = Symbol.for("lit-noChange"), S = Symbol.for("lit-nothing"), pe = /* @__PURE__ */ new WeakMap(), V = j.createTreeWalker(j, 129);
function $e(i, t) {
  if (!Qt(i) || !i.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return he !== void 0 ? he.createHTML(t) : t;
}
const ti = (i, t) => {
  const e = i.length - 1, s = [];
  let n, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = st;
  for (let c = 0; c < e; c++) {
    const a = i[c];
    let l, h, f = -1, d = 0;
    for (; d < a.length && (o.lastIndex = d, h = o.exec(a), h !== null); ) d = o.lastIndex, o === st ? h[1] === "!--" ? o = ue : h[1] !== void 0 ? o = de : h[2] !== void 0 ? (Ae.test(h[2]) && (n = RegExp("</" + h[2], "g")), o = F) : h[3] !== void 0 && (o = F) : o === F ? h[0] === ">" ? (o = n ?? st, f = -1) : h[1] === void 0 ? f = -2 : (f = o.lastIndex - h[2].length, l = h[1], o = h[3] === void 0 ? F : h[3] === '"' ? ge : fe) : o === ge || o === fe ? o = F : o === ue || o === de ? o = st : (o = F, n = void 0);
    const u = o === F && i[c + 1].startsWith("/>") ? " " : "";
    r += o === st ? a + Qe : f >= 0 ? (s.push(l), a.slice(0, f) + Ce + a.slice(f) + x + u) : a + x + (f === -2 ? c : u);
  }
  return [$e(i, r + (i[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class ht {
  constructor({ strings: t, _$litType$: e }, s) {
    let n;
    this.parts = [];
    let r = 0, o = 0;
    const c = t.length - 1, a = this.parts, [l, h] = ti(t, e);
    if (this.el = ht.createElement(l, s), V.currentNode = this.el.content, e === 2 || e === 3) {
      const f = this.el.content.firstChild;
      f.replaceWith(...f.childNodes);
    }
    for (; (n = V.nextNode()) !== null && a.length < c; ) {
      if (n.nodeType === 1) {
        if (n.hasAttributes()) for (const f of n.getAttributeNames()) if (f.endsWith(Ce)) {
          const d = h[o++], u = n.getAttribute(f).split(x), _ = /([.?@])?(.*)/.exec(d);
          a.push({ type: 1, index: r, name: _[2], strings: u, ctor: _[1] === "." ? ii : _[1] === "?" ? ni : _[1] === "@" ? si : Pt }), n.removeAttribute(f);
        } else f.startsWith(x) && (a.push({ type: 6, index: r }), n.removeAttribute(f));
        if (Ae.test(n.tagName)) {
          const f = n.textContent.split(x), d = f.length - 1;
          if (d > 0) {
            n.textContent = At ? At.emptyScript : "";
            for (let u = 0; u < d; u++) n.append(f[u], ct()), V.nextNode(), a.push({ type: 2, index: ++r });
            n.append(f[d], ct());
          }
        }
      } else if (n.nodeType === 8) if (n.data === be) a.push({ type: 2, index: r });
      else {
        let f = -1;
        for (; (f = n.data.indexOf(x, f + 1)) !== -1; ) a.push({ type: 7, index: r }), f += x.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const s = j.createElement("template");
    return s.innerHTML = t, s;
  }
}
function W(i, t, e = i, s) {
  var o, c;
  if (t === J) return t;
  let n = s !== void 0 ? (o = e._$Co) == null ? void 0 : o[s] : e._$Cl;
  const r = lt(t) ? void 0 : t._$litDirective$;
  return (n == null ? void 0 : n.constructor) !== r && ((c = n == null ? void 0 : n._$AO) == null || c.call(n, !1), r === void 0 ? n = void 0 : (n = new r(i), n._$AT(i, e, s)), s !== void 0 ? (e._$Co ?? (e._$Co = []))[s] = n : e._$Cl = n), n !== void 0 && (t = W(i, n._$AS(i, t.values), n, s)), t;
}
class ei {
  constructor(t, e) {
    this._$AV = [], this._$AN = void 0, this._$AD = t, this._$AM = e;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(t) {
    const { el: { content: e }, parts: s } = this._$AD, n = ((t == null ? void 0 : t.creationScope) ?? j).importNode(e, !0);
    V.currentNode = n;
    let r = V.nextNode(), o = 0, c = 0, a = s[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let l;
        a.type === 2 ? l = new mt(r, r.nextSibling, this, t) : a.type === 1 ? l = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (l = new ri(r, this, t)), this._$AV.push(l), a = s[++c];
      }
      o !== (a == null ? void 0 : a.index) && (r = V.nextNode(), o++);
    }
    return V.currentNode = j, n;
  }
  p(t) {
    let e = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, e), e += s.strings.length - 2) : s._$AI(t[e])), e++;
  }
}
class mt {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, s, n) {
    this.type = 2, this._$AH = S, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = n, this._$Cv = (n == null ? void 0 : n.isConnected) ?? !0;
  }
  get parentNode() {
    let t = this._$AA.parentNode;
    const e = this._$AM;
    return e !== void 0 && (t == null ? void 0 : t.nodeType) === 11 && (t = e.parentNode), t;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(t, e = this) {
    t = W(this, t, e), lt(t) ? t === S || t == null || t === "" ? (this._$AH !== S && this._$AR(), this._$AH = S) : t !== this._$AH && t !== J && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : Ze(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== S && lt(this._$AH) ? this._$AA.nextSibling.data = t : this.T(j.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: s } = t, n = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = ht.createElement($e(s.h, s.h[0]), this.options)), s);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === n) this._$AH.p(e);
    else {
      const o = new ei(n, this), c = o.u(this.options);
      o.p(e), this.T(c), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = pe.get(t.strings);
    return e === void 0 && pe.set(t.strings, e = new ht(t)), e;
  }
  k(t) {
    Qt(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, n = 0;
    for (const r of t) n === e.length ? e.push(s = new mt(this.O(ct()), this.O(ct()), this, this.options)) : s = e[n], s._$AI(r), n++;
    n < e.length && (this._$AR(s && s._$AB.nextSibling, n), e.length = n);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, e); t !== this._$AB; ) {
      const n = le(t).nextSibling;
      le(t).remove(), t = n;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class Pt {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, s, n, r) {
    this.type = 1, this._$AH = S, this._$AN = void 0, this.element = t, this.name = e, this._$AM = n, this.options = r, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = S;
  }
  _$AI(t, e = this, s, n) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = W(this, t, e, 0), o = !lt(t) || t !== this._$AH && t !== J, o && (this._$AH = t);
    else {
      const c = t;
      let a, l;
      for (t = r[0], a = 0; a < r.length - 1; a++) l = W(this, c[s + a], e, a), l === J && (l = this._$AH[a]), o || (o = !lt(l) || l !== this._$AH[a]), l === S ? t = S : t !== S && (t += (l ?? "") + r[a + 1]), this._$AH[a] = l;
    }
    o && !n && this.j(t);
  }
  j(t) {
    t === S ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class ii extends Pt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === S ? void 0 : t;
  }
}
class ni extends Pt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== S);
  }
}
class si extends Pt {
  constructor(t, e, s, n, r) {
    super(t, e, s, n, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = W(this, t, e, 0) ?? S) === J) return;
    const s = this._$AH, n = t === S && s !== S || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, r = t !== S && (s === S || n);
    n && this.element.removeEventListener(this.name, this, s), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class ri {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    W(this, t);
  }
}
const xt = ot.litHtmlPolyfillSupport;
xt == null || xt(ht, mt), (ot.litHtmlVersions ?? (ot.litHtmlVersions = [])).push("3.3.2");
const oi = (i, t, e) => {
  const s = (e == null ? void 0 : e.renderBefore) ?? t;
  let n = s._$litPart$;
  if (n === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    s._$litPart$ = n = new mt(t.insertBefore(ct(), r), r, void 0, e ?? {});
  }
  return n._$AI(i), n;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const z = globalThis;
class T extends q {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    var e;
    const t = super.createRenderRoot();
    return (e = this.renderOptions).renderBefore ?? (e.renderBefore = t.firstChild), t;
  }
  update(t) {
    const e = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = oi(e, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    var t;
    super.connectedCallback(), (t = this._$Do) == null || t.setConnected(!0);
  }
  disconnectedCallback() {
    var t;
    super.disconnectedCallback(), (t = this._$Do) == null || t.setConnected(!1);
  }
  render() {
    return J;
  }
}
var ve;
T._$litElement$ = !0, T.finalized = !0, (ve = z.litElementHydrateSupport) == null || ve.call(z, { LitElement: T });
const Ut = z.litElementPolyfillSupport;
Ut == null || Ut({ LitElement: T });
(z.litElementVersions ?? (z.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const tt = (i) => (t, e) => {
  e !== void 0 ? e.addInitializer(() => {
    customElements.define(i, t);
  }) : customElements.define(i, t);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ai = { attribute: !0, type: String, converter: bt, reflect: !1, hasChanged: Yt }, ci = (i = ai, t, e) => {
  const { kind: s, metadata: n } = e;
  let r = globalThis.litPropertyMetadata.get(n);
  if (r === void 0 && globalThis.litPropertyMetadata.set(n, r = /* @__PURE__ */ new Map()), s === "setter" && ((i = Object.create(i)).wrapped = !0), r.set(e.name, i), s === "accessor") {
    const { name: o } = e;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(o, a, i, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(o, void 0, i, c), c;
    } };
  }
  if (s === "setter") {
    const { name: o } = e;
    return function(c) {
      const a = this[o];
      t.call(this, c), this.requestUpdate(o, a, i, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + s);
};
function O(i) {
  return (t, e) => typeof e == "object" ? ci(i, t, e) : ((s, n, r) => {
    const o = n.hasOwnProperty(r);
    return n.constructor.createProperty(r, s), o ? Object.getOwnPropertyDescriptor(n, r) : void 0;
  })(i, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function b(i) {
  return O({ ...i, state: !0, attribute: !1 });
}
var li = Object.defineProperty, hi = Object.getOwnPropertyDescriptor, et = (i, t, e, s) => {
  for (var n = s > 1 ? void 0 : s ? hi(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (n = (s ? o(t, e, n) : o(n)) || n);
  return s && n && li(t, e, n), n;
};
let ut = class extends T {
  static async getConfigElement() {
    return document.createElement("meraki-content-filter-card-editor");
  }
  setConfig(i) {
    if (!i || !i.entity)
      throw new Error("Please define a Meraki content filter entity");
    this._config = i;
  }
  static getStubConfig() {
    return {
      entity: "select.meraki_network_content_filter",
      name: "Meraki Content Filter"
    };
  }
  render() {
    if (!this._config || !this.hass)
      return E``;
    const i = this._config.entity, t = this.hass.states[i];
    if (!t)
      return E`
        <ha-card>
          <div class="card-content">
            <ha-alert alert-type="error">Entity not found: ${i}</ha-alert>
          </div>
        </ha-card>
      `;
    const e = t.state, s = t.attributes.options || ["None", "Security", "Family", "Strict"], n = this._config.name || t.attributes.friendly_name || "Content Filter";
    return E`
      <ha-card>
        <div class="card-header">${n}</div>
        <div class="card-content">
          <div class="current-profile">
            Current Profile: <strong>${e}</strong>
          </div>
          <div class="profile-buttons">
            ${s.map((r) => E`
              <div
                class="profile-button ${e === r ? "active" : ""}"
                @click="${() => this._handleProfileSelect(r)}"
              >
                <span class="profile-name">${r}</span>
              </div>
            `)}
          </div>
        </div>
      </ha-card>
    `;
  }
  async _handleProfileSelect(i) {
    if (!(!this.hass || !this._config))
      try {
        await this.hass.callService("select", "select_option", {
          entity_id: this._config.entity,
          option: i
        });
      } catch (t) {
        console.error("Failed to call select_option service:", t);
      }
  }
};
ut.styles = G`
    :host {
      display: block;
    }
    ha-card {
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-header {
      padding: 16px 16px 0;
      font-size: 24px;
      line-height: 1.2;
    }
    .card-content {
      padding: 16px;
    }
    .network-name {
      font-weight: 500;
      margin-bottom: 4px;
    }
    .current-profile {
      color: var(--secondary-text-color);
      font-size: 0.9em;
      margin-bottom: 16px;
    }
    .profile-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .profile-button {
      flex: 1 1 calc(50% - 4px);
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-theme-on-primary: var(--card-background-color);
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      padding: 8px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      background-color: var(--card-background-color);
    }
    .profile-button:hover {
      background-color: var(--secondary-background-color);
    }
    .profile-button.active {
      background-color: var(--primary-color);
      color: var(--text-primary-color);
      border-color: var(--primary-color);
    }
    .profile-button.active .profile-name {
       color: var(--text-primary-color);
    }
    .profile-name {
      font-weight: bold;
      display: block;
    }
  `;
et([
  O({ attribute: !1 })
], ut.prototype, "hass", 2);
et([
  b()
], ut.prototype, "_config", 2);
ut = et([
  tt("meraki-content-filter-card")
], ut);
let dt = class extends T {
  setConfig(i) {
    this._config = i;
  }
  render() {
    return !this.hass || !this._config ? E`` : E`
      <div class="card-config">
        <ha-entity-picker
          .hass=${this.hass}
          .value=${this._config.entity}
          .configValue=${"entity"}
          .includeDomains=${["select"]}
          @value-changed=${this._valueChanged}
          allow-custom-entity
          label="Entity (Required)"
        ></ha-entity-picker>
        <ha-textfield
          label="Name (Optional)"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }
  _valueChanged(i) {
    if (!this._config || !this.hass)
      return;
    const t = i.target, e = t.configValue;
    if (!e)
      return;
    let s = t.value;
    if (this._config[e] === s)
      return;
    const n = { ...this._config };
    s === "" || s === void 0 ? delete n[e] : n[e] = s, this._config = n;
    const r = new CustomEvent("config-changed", {
      detail: { config: this._config },
      bubbles: !0,
      composed: !0
    });
    this.dispatchEvent(r);
  }
};
dt.styles = G`
    .card-config ha-entity-picker,
    .card-config ha-textfield {
      display: block;
      margin-bottom: 16px;
    }
  `;
et([
  O({ attribute: !1 })
], dt.prototype, "hass", 2);
et([
  b()
], dt.prototype, "_config", 2);
dt = et([
  tt("meraki-content-filter-card-editor")
], dt);
window.customCards = window.customCards || [];
window.customCards.some((i) => i.type === "meraki-content-filter-card") || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var yt = {}, ui = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, Se = {}, N = {};
let Zt;
const di = [
  0,
  // Not used
  26,
  44,
  70,
  100,
  134,
  172,
  196,
  242,
  292,
  346,
  404,
  466,
  532,
  581,
  655,
  733,
  815,
  901,
  991,
  1085,
  1156,
  1258,
  1364,
  1474,
  1588,
  1706,
  1828,
  1921,
  2051,
  2185,
  2323,
  2465,
  2611,
  2761,
  2876,
  3034,
  3196,
  3362,
  3532,
  3706
];
N.getSymbolSize = function(t) {
  if (!t) throw new Error('"version" cannot be null or undefined');
  if (t < 1 || t > 40) throw new Error('"version" should be in range from 1 to 40');
  return t * 4 + 17;
};
N.getSymbolTotalCodewords = function(t) {
  return di[t];
};
N.getBCHDigit = function(i) {
  let t = 0;
  for (; i !== 0; )
    t++, i >>>= 1;
  return t;
};
N.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  Zt = t;
};
N.isKanjiModeEnabled = function() {
  return typeof Zt < "u";
};
N.toSJIS = function(t) {
  return Zt(t);
};
var kt = {};
(function(i) {
  i.L = { bit: 1 }, i.M = { bit: 0 }, i.Q = { bit: 3 }, i.H = { bit: 2 };
  function t(e) {
    if (typeof e != "string")
      throw new Error("Param is not a string");
    switch (e.toLowerCase()) {
      case "l":
      case "low":
        return i.L;
      case "m":
      case "medium":
        return i.M;
      case "q":
      case "quartile":
        return i.Q;
      case "h":
      case "high":
        return i.H;
      default:
        throw new Error("Unknown EC Level: " + e);
    }
  }
  i.isValid = function(s) {
    return s && typeof s.bit < "u" && s.bit >= 0 && s.bit < 4;
  }, i.from = function(s, n) {
    if (i.isValid(s))
      return s;
    try {
      return t(s);
    } catch {
      return n;
    }
  };
})(kt);
function Pe() {
  this.buffer = [], this.length = 0;
}
Pe.prototype = {
  get: function(i) {
    const t = Math.floor(i / 8);
    return (this.buffer[t] >>> 7 - i % 8 & 1) === 1;
  },
  put: function(i, t) {
    for (let e = 0; e < t; e++)
      this.putBit((i >>> t - e - 1 & 1) === 1);
  },
  getLengthInBits: function() {
    return this.length;
  },
  putBit: function(i) {
    const t = Math.floor(this.length / 8);
    this.buffer.length <= t && this.buffer.push(0), i && (this.buffer[t] |= 128 >>> this.length % 8), this.length++;
  }
};
var fi = Pe;
function wt(i) {
  if (!i || i < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = i, this.data = new Uint8Array(i * i), this.reservedBit = new Uint8Array(i * i);
}
wt.prototype.set = function(i, t, e, s) {
  const n = i * this.size + t;
  this.data[n] = e, s && (this.reservedBit[n] = !0);
};
wt.prototype.get = function(i, t) {
  return this.data[i * this.size + t];
};
wt.prototype.xor = function(i, t, e) {
  this.data[i * this.size + t] ^= e;
};
wt.prototype.isReserved = function(i, t) {
  return this.reservedBit[i * this.size + t];
};
var gi = wt, ke = {};
(function(i) {
  const t = N.getSymbolSize;
  i.getRowColCoords = function(s) {
    if (s === 1) return [];
    const n = Math.floor(s / 7) + 2, r = t(s), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * n - 2)) * 2, c = [r - 7];
    for (let a = 1; a < n - 1; a++)
      c[a] = c[a - 1] - o;
    return c.push(6), c.reverse();
  }, i.getPositions = function(s) {
    const n = [], r = i.getRowColCoords(s), o = r.length;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        c === 0 && a === 0 || // top-left
        c === 0 && a === o - 1 || // bottom-left
        c === o - 1 && a === 0 || n.push([r[c], r[a]]);
    return n;
  };
})(ke);
var Ne = {};
const pi = N.getSymbolSize, _e = 7;
Ne.getPositions = function(t) {
  const e = pi(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - _e, 0],
    // bottom-left
    [0, e - _e]
  ];
};
var Me = {};
(function(i) {
  i.Patterns = {
    PATTERN000: 0,
    PATTERN001: 1,
    PATTERN010: 2,
    PATTERN011: 3,
    PATTERN100: 4,
    PATTERN101: 5,
    PATTERN110: 6,
    PATTERN111: 7
  };
  const t = {
    N1: 3,
    N2: 3,
    N3: 40,
    N4: 10
  };
  i.isValid = function(n) {
    return n != null && n !== "" && !isNaN(n) && n >= 0 && n <= 7;
  }, i.from = function(n) {
    return i.isValid(n) ? parseInt(n, 10) : void 0;
  }, i.getPenaltyN1 = function(n) {
    const r = n.size;
    let o = 0, c = 0, a = 0, l = null, h = null;
    for (let f = 0; f < r; f++) {
      c = a = 0, l = h = null;
      for (let d = 0; d < r; d++) {
        let u = n.get(f, d);
        u === l ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), l = u, c = 1), u = n.get(d, f), u === h ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), h = u, a = 1);
      }
      c >= 5 && (o += t.N1 + (c - 5)), a >= 5 && (o += t.N1 + (a - 5));
    }
    return o;
  }, i.getPenaltyN2 = function(n) {
    const r = n.size;
    let o = 0;
    for (let c = 0; c < r - 1; c++)
      for (let a = 0; a < r - 1; a++) {
        const l = n.get(c, a) + n.get(c, a + 1) + n.get(c + 1, a) + n.get(c + 1, a + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, i.getPenaltyN3 = function(n) {
    const r = n.size;
    let o = 0, c = 0, a = 0;
    for (let l = 0; l < r; l++) {
      c = a = 0;
      for (let h = 0; h < r; h++)
        c = c << 1 & 2047 | n.get(l, h), h >= 10 && (c === 1488 || c === 93) && o++, a = a << 1 & 2047 | n.get(h, l), h >= 10 && (a === 1488 || a === 93) && o++;
    }
    return o * t.N3;
  }, i.getPenaltyN4 = function(n) {
    let r = 0;
    const o = n.data.length;
    for (let a = 0; a < o; a++) r += n.data[a];
    return Math.abs(Math.ceil(r * 100 / o / 5) - 10) * t.N4;
  };
  function e(s, n, r) {
    switch (s) {
      case i.Patterns.PATTERN000:
        return (n + r) % 2 === 0;
      case i.Patterns.PATTERN001:
        return n % 2 === 0;
      case i.Patterns.PATTERN010:
        return r % 3 === 0;
      case i.Patterns.PATTERN011:
        return (n + r) % 3 === 0;
      case i.Patterns.PATTERN100:
        return (Math.floor(n / 2) + Math.floor(r / 3)) % 2 === 0;
      case i.Patterns.PATTERN101:
        return n * r % 2 + n * r % 3 === 0;
      case i.Patterns.PATTERN110:
        return (n * r % 2 + n * r % 3) % 2 === 0;
      case i.Patterns.PATTERN111:
        return (n * r % 3 + (n + r) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + s);
    }
  }
  i.applyMask = function(n, r) {
    const o = r.size;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        r.isReserved(a, c) || r.xor(a, c, e(n, a, c));
  }, i.getBestMask = function(n, r) {
    const o = Object.keys(i.Patterns).length;
    let c = 0, a = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), i.applyMask(l, n);
      const h = i.getPenaltyN1(n) + i.getPenaltyN2(n) + i.getPenaltyN3(n) + i.getPenaltyN4(n);
      i.applyMask(l, n), h < a && (a = h, c = l);
    }
    return c;
  };
})(Me);
var Nt = {};
const U = kt, vt = [
  // L  M  Q  H
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  2,
  1,
  2,
  2,
  4,
  1,
  2,
  4,
  4,
  2,
  4,
  4,
  4,
  2,
  4,
  6,
  5,
  2,
  4,
  6,
  6,
  2,
  5,
  8,
  8,
  4,
  5,
  8,
  8,
  4,
  5,
  8,
  11,
  4,
  8,
  10,
  11,
  4,
  9,
  12,
  16,
  4,
  9,
  16,
  16,
  6,
  10,
  12,
  18,
  6,
  10,
  17,
  16,
  6,
  11,
  16,
  19,
  6,
  13,
  18,
  21,
  7,
  14,
  21,
  25,
  8,
  16,
  20,
  25,
  8,
  17,
  23,
  25,
  9,
  17,
  23,
  34,
  9,
  18,
  25,
  30,
  10,
  20,
  27,
  32,
  12,
  21,
  29,
  35,
  12,
  23,
  34,
  37,
  12,
  25,
  34,
  40,
  13,
  26,
  35,
  42,
  14,
  28,
  38,
  45,
  15,
  29,
  40,
  48,
  16,
  31,
  43,
  51,
  17,
  33,
  45,
  54,
  18,
  35,
  48,
  57,
  19,
  37,
  51,
  60,
  19,
  38,
  53,
  63,
  20,
  40,
  56,
  66,
  21,
  43,
  59,
  70,
  22,
  45,
  62,
  74,
  24,
  47,
  65,
  77,
  25,
  49,
  68,
  81
], Et = [
  // L  M  Q  H
  7,
  10,
  13,
  17,
  10,
  16,
  22,
  28,
  15,
  26,
  36,
  44,
  20,
  36,
  52,
  64,
  26,
  48,
  72,
  88,
  36,
  64,
  96,
  112,
  40,
  72,
  108,
  130,
  48,
  88,
  132,
  156,
  60,
  110,
  160,
  192,
  72,
  130,
  192,
  224,
  80,
  150,
  224,
  264,
  96,
  176,
  260,
  308,
  104,
  198,
  288,
  352,
  120,
  216,
  320,
  384,
  132,
  240,
  360,
  432,
  144,
  280,
  408,
  480,
  168,
  308,
  448,
  532,
  180,
  338,
  504,
  588,
  196,
  364,
  546,
  650,
  224,
  416,
  600,
  700,
  224,
  442,
  644,
  750,
  252,
  476,
  690,
  816,
  270,
  504,
  750,
  900,
  300,
  560,
  810,
  960,
  312,
  588,
  870,
  1050,
  336,
  644,
  952,
  1110,
  360,
  700,
  1020,
  1200,
  390,
  728,
  1050,
  1260,
  420,
  784,
  1140,
  1350,
  450,
  812,
  1200,
  1440,
  480,
  868,
  1290,
  1530,
  510,
  924,
  1350,
  1620,
  540,
  980,
  1440,
  1710,
  570,
  1036,
  1530,
  1800,
  570,
  1064,
  1590,
  1890,
  600,
  1120,
  1680,
  1980,
  630,
  1204,
  1770,
  2100,
  660,
  1260,
  1860,
  2220,
  720,
  1316,
  1950,
  2310,
  750,
  1372,
  2040,
  2430
];
Nt.getBlocksCount = function(t, e) {
  switch (e) {
    case U.L:
      return vt[(t - 1) * 4 + 0];
    case U.M:
      return vt[(t - 1) * 4 + 1];
    case U.Q:
      return vt[(t - 1) * 4 + 2];
    case U.H:
      return vt[(t - 1) * 4 + 3];
    default:
      return;
  }
};
Nt.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case U.L:
      return Et[(t - 1) * 4 + 0];
    case U.M:
      return Et[(t - 1) * 4 + 1];
    case U.Q:
      return Et[(t - 1) * 4 + 2];
    case U.H:
      return Et[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var Te = {}, Mt = {};
const at = new Uint8Array(512), $t = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    at[e] = t, $t[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    at[e] = at[e - 255];
})();
Mt.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return $t[t];
};
Mt.exp = function(t) {
  return at[t];
};
Mt.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : at[$t[t] + $t[e]];
};
(function(i) {
  const t = Mt;
  i.mul = function(s, n) {
    const r = new Uint8Array(s.length + n.length - 1);
    for (let o = 0; o < s.length; o++)
      for (let c = 0; c < n.length; c++)
        r[o + c] ^= t.mul(s[o], n[c]);
    return r;
  }, i.mod = function(s, n) {
    let r = new Uint8Array(s);
    for (; r.length - n.length >= 0; ) {
      const o = r[0];
      for (let a = 0; a < n.length; a++)
        r[a] ^= t.mul(n[a], o);
      let c = 0;
      for (; c < r.length && r[c] === 0; ) c++;
      r = r.slice(c);
    }
    return r;
  }, i.generateECPolynomial = function(s) {
    let n = new Uint8Array([1]);
    for (let r = 0; r < s; r++)
      n = i.mul(n, new Uint8Array([1, t.exp(r)]));
    return n;
  };
})(Te);
const Ie = Te;
function Xt(i) {
  this.genPoly = void 0, this.degree = i, this.degree && this.initialize(this.degree);
}
Xt.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = Ie.generateECPolynomial(this.degree);
};
Xt.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const s = Ie.mod(e, this.genPoly), n = this.degree - s.length;
  if (n > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(s, n), r;
  }
  return s;
};
var _i = Xt, Be = {}, H = {}, te = {};
te.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var B = {};
const Re = "[0-9]+", mi = "[A-Z $%*+\\-./:]+";
let ft = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
ft = ft.replace(/u/g, "\\u");
const yi = "(?:(?![A-Z0-9 $%*+\\-./:]|" + ft + `)(?:.|[\r
]))+`;
B.KANJI = new RegExp(ft, "g");
B.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
B.BYTE = new RegExp(yi, "g");
B.NUMERIC = new RegExp(Re, "g");
B.ALPHANUMERIC = new RegExp(mi, "g");
const wi = new RegExp("^" + ft + "$"), vi = new RegExp("^" + Re + "$"), Ei = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
B.testKanji = function(t) {
  return wi.test(t);
};
B.testNumeric = function(t) {
  return vi.test(t);
};
B.testAlphanumeric = function(t) {
  return Ei.test(t);
};
(function(i) {
  const t = te, e = B;
  i.NUMERIC = {
    id: "Numeric",
    bit: 1,
    ccBits: [10, 12, 14]
  }, i.ALPHANUMERIC = {
    id: "Alphanumeric",
    bit: 2,
    ccBits: [9, 11, 13]
  }, i.BYTE = {
    id: "Byte",
    bit: 4,
    ccBits: [8, 16, 16]
  }, i.KANJI = {
    id: "Kanji",
    bit: 8,
    ccBits: [8, 10, 12]
  }, i.MIXED = {
    bit: -1
  }, i.getCharCountIndicator = function(r, o) {
    if (!r.ccBits) throw new Error("Invalid mode: " + r);
    if (!t.isValid(o))
      throw new Error("Invalid version: " + o);
    return o >= 1 && o < 10 ? r.ccBits[0] : o < 27 ? r.ccBits[1] : r.ccBits[2];
  }, i.getBestModeForData = function(r) {
    return e.testNumeric(r) ? i.NUMERIC : e.testAlphanumeric(r) ? i.ALPHANUMERIC : e.testKanji(r) ? i.KANJI : i.BYTE;
  }, i.toString = function(r) {
    if (r && r.id) return r.id;
    throw new Error("Invalid mode");
  }, i.isValid = function(r) {
    return r && r.bit && r.ccBits;
  };
  function s(n) {
    if (typeof n != "string")
      throw new Error("Param is not a string");
    switch (n.toLowerCase()) {
      case "numeric":
        return i.NUMERIC;
      case "alphanumeric":
        return i.ALPHANUMERIC;
      case "kanji":
        return i.KANJI;
      case "byte":
        return i.BYTE;
      default:
        throw new Error("Unknown mode: " + n);
    }
  }
  i.from = function(r, o) {
    if (i.isValid(r))
      return r;
    try {
      return s(r);
    } catch {
      return o;
    }
  };
})(H);
(function(i) {
  const t = N, e = Nt, s = kt, n = H, r = te, o = 7973, c = t.getBCHDigit(o);
  function a(d, u, _) {
    for (let y = 1; y <= 40; y++)
      if (u <= i.getCapacity(y, _, d))
        return y;
  }
  function l(d, u) {
    return n.getCharCountIndicator(d, u) + 4;
  }
  function h(d, u) {
    let _ = 0;
    return d.forEach(function(y) {
      const P = l(y.mode, u);
      _ += P + y.getBitsLength();
    }), _;
  }
  function f(d, u) {
    for (let _ = 1; _ <= 40; _++)
      if (h(d, _) <= i.getCapacity(_, u, n.MIXED))
        return _;
  }
  i.from = function(u, _) {
    return r.isValid(u) ? parseInt(u, 10) : _;
  }, i.getCapacity = function(u, _, y) {
    if (!r.isValid(u))
      throw new Error("Invalid QR Code version");
    typeof y > "u" && (y = n.BYTE);
    const P = t.getSymbolTotalCodewords(u), m = e.getTotalCodewordsCount(u, _), w = (P - m) * 8;
    if (y === n.MIXED) return w;
    const p = w - l(y, u);
    switch (y) {
      case n.NUMERIC:
        return Math.floor(p / 10 * 3);
      case n.ALPHANUMERIC:
        return Math.floor(p / 11 * 2);
      case n.KANJI:
        return Math.floor(p / 13);
      case n.BYTE:
      default:
        return Math.floor(p / 8);
    }
  }, i.getBestVersionForData = function(u, _) {
    let y;
    const P = s.from(_, s.M);
    if (Array.isArray(u)) {
      if (u.length > 1)
        return f(u, P);
      if (u.length === 0)
        return 1;
      y = u[0];
    } else
      y = u;
    return a(y.mode, y.getLength(), P);
  }, i.getEncodedBits = function(u) {
    if (!r.isValid(u) || u < 7)
      throw new Error("Invalid QR Code version");
    let _ = u << 12;
    for (; t.getBCHDigit(_) - c >= 0; )
      _ ^= o << t.getBCHDigit(_) - c;
    return u << 12 | _;
  };
})(Be);
var De = {};
const zt = N, xe = 1335, Ci = 21522, me = zt.getBCHDigit(xe);
De.getEncodedBits = function(t, e) {
  const s = t.bit << 3 | e;
  let n = s << 10;
  for (; zt.getBCHDigit(n) - me >= 0; )
    n ^= xe << zt.getBCHDigit(n) - me;
  return (s << 10 | n) ^ Ci;
};
var Ue = {};
const bi = H;
function Y(i) {
  this.mode = bi.NUMERIC, this.data = i.toString();
}
Y.getBitsLength = function(t) {
  return 10 * Math.floor(t / 3) + (t % 3 ? t % 3 * 3 + 1 : 0);
};
Y.prototype.getLength = function() {
  return this.data.length;
};
Y.prototype.getBitsLength = function() {
  return Y.getBitsLength(this.data.length);
};
Y.prototype.write = function(t) {
  let e, s, n;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    s = this.data.substr(e, 3), n = parseInt(s, 10), t.put(n, 10);
  const r = this.data.length - e;
  r > 0 && (s = this.data.substr(e), n = parseInt(s, 10), t.put(n, r * 3 + 1));
};
var Ai = Y;
const $i = H, Lt = [
  "0",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "K",
  "L",
  "M",
  "N",
  "O",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "U",
  "V",
  "W",
  "X",
  "Y",
  "Z",
  " ",
  "$",
  "%",
  "*",
  "+",
  "-",
  ".",
  "/",
  ":"
];
function Q(i) {
  this.mode = $i.ALPHANUMERIC, this.data = i;
}
Q.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
Q.prototype.getLength = function() {
  return this.data.length;
};
Q.prototype.getBitsLength = function() {
  return Q.getBitsLength(this.data.length);
};
Q.prototype.write = function(t) {
  let e;
  for (e = 0; e + 2 <= this.data.length; e += 2) {
    let s = Lt.indexOf(this.data[e]) * 45;
    s += Lt.indexOf(this.data[e + 1]), t.put(s, 11);
  }
  this.data.length % 2 && t.put(Lt.indexOf(this.data[e]), 6);
};
var Si = Q;
const Pi = H;
function Z(i) {
  this.mode = Pi.BYTE, typeof i == "string" ? this.data = new TextEncoder().encode(i) : this.data = new Uint8Array(i);
}
Z.getBitsLength = function(t) {
  return t * 8;
};
Z.prototype.getLength = function() {
  return this.data.length;
};
Z.prototype.getBitsLength = function() {
  return Z.getBitsLength(this.data.length);
};
Z.prototype.write = function(i) {
  for (let t = 0, e = this.data.length; t < e; t++)
    i.put(this.data[t], 8);
};
var ki = Z;
const Ni = H, Mi = N;
function X(i) {
  this.mode = Ni.KANJI, this.data = i;
}
X.getBitsLength = function(t) {
  return t * 13;
};
X.prototype.getLength = function() {
  return this.data.length;
};
X.prototype.getBitsLength = function() {
  return X.getBitsLength(this.data.length);
};
X.prototype.write = function(i) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let e = Mi.toSJIS(this.data[t]);
    if (e >= 33088 && e <= 40956)
      e -= 33088;
    else if (e >= 57408 && e <= 60351)
      e -= 49472;
    else
      throw new Error(
        "Invalid SJIS character: " + this.data[t] + `
Make sure your charset is UTF-8`
      );
    e = (e >>> 8 & 255) * 192 + (e & 255), i.put(e, 13);
  }
};
var Ti = X, Le = { exports: {} };
(function(i) {
  var t = {
    single_source_shortest_paths: function(e, s, n) {
      var r = {}, o = {};
      o[s] = 0;
      var c = t.PriorityQueue.make();
      c.push(s, 0);
      for (var a, l, h, f, d, u, _, y, P; !c.empty(); ) {
        a = c.pop(), l = a.value, f = a.cost, d = e[l] || {};
        for (h in d)
          d.hasOwnProperty(h) && (u = d[h], _ = f + u, y = o[h], P = typeof o[h] > "u", (P || y > _) && (o[h] = _, c.push(h, _), r[h] = l));
      }
      if (typeof n < "u" && typeof o[n] > "u") {
        var m = ["Could not find a path from ", s, " to ", n, "."].join("");
        throw new Error(m);
      }
      return r;
    },
    extract_shortest_path_from_predecessor_list: function(e, s) {
      for (var n = [], r = s; r; )
        n.push(r), e[r], r = e[r];
      return n.reverse(), n;
    },
    find_path: function(e, s, n) {
      var r = t.single_source_shortest_paths(e, s, n);
      return t.extract_shortest_path_from_predecessor_list(
        r,
        n
      );
    },
    /**
     * A very naive priority queue implementation.
     */
    PriorityQueue: {
      make: function(e) {
        var s = t.PriorityQueue, n = {}, r;
        e = e || {};
        for (r in s)
          s.hasOwnProperty(r) && (n[r] = s[r]);
        return n.queue = [], n.sorter = e.sorter || s.default_sorter, n;
      },
      default_sorter: function(e, s) {
        return e.cost - s.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(e, s) {
        var n = { value: e, cost: s };
        this.queue.push(n), this.queue.sort(this.sorter);
      },
      /**
       * Return the highest priority element in the queue.
       */
      pop: function() {
        return this.queue.shift();
      },
      empty: function() {
        return this.queue.length === 0;
      }
    }
  };
  i.exports = t;
})(Le);
var Ii = Le.exports;
(function(i) {
  const t = H, e = Ai, s = Si, n = ki, r = Ti, o = B, c = N, a = Ii;
  function l(m) {
    return unescape(encodeURIComponent(m)).length;
  }
  function h(m, w, p) {
    const g = [];
    let v;
    for (; (v = m.exec(p)) !== null; )
      g.push({
        data: v[0],
        index: v.index,
        mode: w,
        length: v[0].length
      });
    return g;
  }
  function f(m) {
    const w = h(o.NUMERIC, t.NUMERIC, m), p = h(o.ALPHANUMERIC, t.ALPHANUMERIC, m);
    let g, v;
    return c.isKanjiModeEnabled() ? (g = h(o.BYTE, t.BYTE, m), v = h(o.KANJI, t.KANJI, m)) : (g = h(o.BYTE_KANJI, t.BYTE, m), v = []), w.concat(p, g, v).sort(function($, M) {
      return $.index - M.index;
    }).map(function($) {
      return {
        data: $.data,
        mode: $.mode,
        length: $.length
      };
    });
  }
  function d(m, w) {
    switch (w) {
      case t.NUMERIC:
        return e.getBitsLength(m);
      case t.ALPHANUMERIC:
        return s.getBitsLength(m);
      case t.KANJI:
        return r.getBitsLength(m);
      case t.BYTE:
        return n.getBitsLength(m);
    }
  }
  function u(m) {
    return m.reduce(function(w, p) {
      const g = w.length - 1 >= 0 ? w[w.length - 1] : null;
      return g && g.mode === p.mode ? (w[w.length - 1].data += p.data, w) : (w.push(p), w);
    }, []);
  }
  function _(m) {
    const w = [];
    for (let p = 0; p < m.length; p++) {
      const g = m[p];
      switch (g.mode) {
        case t.NUMERIC:
          w.push([
            g,
            { data: g.data, mode: t.ALPHANUMERIC, length: g.length },
            { data: g.data, mode: t.BYTE, length: g.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          w.push([
            g,
            { data: g.data, mode: t.BYTE, length: g.length }
          ]);
          break;
        case t.KANJI:
          w.push([
            g,
            { data: g.data, mode: t.BYTE, length: l(g.data) }
          ]);
          break;
        case t.BYTE:
          w.push([
            { data: g.data, mode: t.BYTE, length: l(g.data) }
          ]);
      }
    }
    return w;
  }
  function y(m, w) {
    const p = {}, g = { start: {} };
    let v = ["start"];
    for (let C = 0; C < m.length; C++) {
      const $ = m[C], M = [];
      for (let D = 0; D < $.length; D++) {
        const I = $[D], nt = "" + C + D;
        M.push(nt), p[nt] = { node: I, lastCount: 0 }, g[nt] = {};
        for (let Bt = 0; Bt < v.length; Bt++) {
          const R = v[Bt];
          p[R] && p[R].node.mode === I.mode ? (g[R][nt] = d(p[R].lastCount + I.length, I.mode) - d(p[R].lastCount, I.mode), p[R].lastCount += I.length) : (p[R] && (p[R].lastCount = I.length), g[R][nt] = d(I.length, I.mode) + 4 + t.getCharCountIndicator(I.mode, w));
        }
      }
      v = M;
    }
    for (let C = 0; C < v.length; C++)
      g[v[C]].end = 0;
    return { map: g, table: p };
  }
  function P(m, w) {
    let p;
    const g = t.getBestModeForData(m);
    if (p = t.from(w, g), p !== t.BYTE && p.bit < g.bit)
      throw new Error('"' + m + '" cannot be encoded with mode ' + t.toString(p) + `.
 Suggested mode is: ` + t.toString(g));
    switch (p === t.KANJI && !c.isKanjiModeEnabled() && (p = t.BYTE), p) {
      case t.NUMERIC:
        return new e(m);
      case t.ALPHANUMERIC:
        return new s(m);
      case t.KANJI:
        return new r(m);
      case t.BYTE:
        return new n(m);
    }
  }
  i.fromArray = function(w) {
    return w.reduce(function(p, g) {
      return typeof g == "string" ? p.push(P(g, null)) : g.data && p.push(P(g.data, g.mode)), p;
    }, []);
  }, i.fromString = function(w, p) {
    const g = f(w, c.isKanjiModeEnabled()), v = _(g), C = y(v, p), $ = a.find_path(C.map, "start", "end"), M = [];
    for (let D = 1; D < $.length - 1; D++)
      M.push(C.table[$[D]].node);
    return i.fromArray(u(M));
  }, i.rawSplit = function(w) {
    return i.fromArray(
      f(w, c.isKanjiModeEnabled())
    );
  };
})(Ue);
const Tt = N, Ot = kt, Bi = fi, Ri = gi, Di = ke, xi = Ne, jt = Me, Kt = Nt, Ui = _i, St = Be, Li = De, Oi = H, Ht = Ue;
function Hi(i, t) {
  const e = i.size, s = xi.getPositions(t);
  for (let n = 0; n < s.length; n++) {
    const r = s[n][0], o = s[n][1];
    for (let c = -1; c <= 7; c++)
      if (!(r + c <= -1 || e <= r + c))
        for (let a = -1; a <= 7; a++)
          o + a <= -1 || e <= o + a || (c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 2 && c <= 4 && a >= 2 && a <= 4 ? i.set(r + c, o + a, !0, !0) : i.set(r + c, o + a, !1, !0));
  }
}
function Fi(i) {
  const t = i.size;
  for (let e = 8; e < t - 8; e++) {
    const s = e % 2 === 0;
    i.set(e, 6, s, !0), i.set(6, e, s, !0);
  }
}
function Vi(i, t) {
  const e = Di.getPositions(t);
  for (let s = 0; s < e.length; s++) {
    const n = e[s][0], r = e[s][1];
    for (let o = -2; o <= 2; o++)
      for (let c = -2; c <= 2; c++)
        o === -2 || o === 2 || c === -2 || c === 2 || o === 0 && c === 0 ? i.set(n + o, r + c, !0, !0) : i.set(n + o, r + c, !1, !0);
  }
}
function zi(i, t) {
  const e = i.size, s = St.getEncodedBits(t);
  let n, r, o;
  for (let c = 0; c < 18; c++)
    n = Math.floor(c / 3), r = c % 3 + e - 8 - 3, o = (s >> c & 1) === 1, i.set(n, r, o, !0), i.set(r, n, o, !0);
}
function Ft(i, t, e) {
  const s = i.size, n = Li.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (n >> r & 1) === 1, r < 6 ? i.set(r, 8, o, !0) : r < 8 ? i.set(r + 1, 8, o, !0) : i.set(s - 15 + r, 8, o, !0), r < 8 ? i.set(8, s - r - 1, o, !0) : r < 9 ? i.set(8, 15 - r - 1 + 1, o, !0) : i.set(8, 15 - r - 1, o, !0);
  i.set(s - 8, 8, 1, !0);
}
function ji(i, t) {
  const e = i.size;
  let s = -1, n = e - 1, r = 7, o = 0;
  for (let c = e - 1; c > 0; c -= 2)
    for (c === 6 && c--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!i.isReserved(n, c - a)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), i.set(n, c - a, l), r--, r === -1 && (o++, r = 7);
        }
      if (n += s, n < 0 || e <= n) {
        n -= s, s = -s;
        break;
      }
    }
}
function Ki(i, t, e) {
  const s = new Bi();
  e.forEach(function(a) {
    s.put(a.mode.bit, 4), s.put(a.getLength(), Oi.getCharCountIndicator(a.mode, i)), a.write(s);
  });
  const n = Tt.getSymbolTotalCodewords(i), r = Kt.getTotalCodewordsCount(i, t), o = (n - r) * 8;
  for (s.getLengthInBits() + 4 <= o && s.put(0, 4); s.getLengthInBits() % 8 !== 0; )
    s.putBit(0);
  const c = (o - s.getLengthInBits()) / 8;
  for (let a = 0; a < c; a++)
    s.put(a % 2 ? 17 : 236, 8);
  return Gi(s, i, t);
}
function Gi(i, t, e) {
  const s = Tt.getSymbolTotalCodewords(t), n = Kt.getTotalCodewordsCount(t, e), r = s - n, o = Kt.getBlocksCount(t, e), c = s % o, a = o - c, l = Math.floor(s / o), h = Math.floor(r / o), f = h + 1, d = l - h, u = new Ui(d);
  let _ = 0;
  const y = new Array(o), P = new Array(o);
  let m = 0;
  const w = new Uint8Array(i.buffer);
  for (let $ = 0; $ < o; $++) {
    const M = $ < a ? h : f;
    y[$] = w.slice(_, _ + M), P[$] = u.encode(y[$]), _ += M, m = Math.max(m, M);
  }
  const p = new Uint8Array(s);
  let g = 0, v, C;
  for (v = 0; v < m; v++)
    for (C = 0; C < o; C++)
      v < y[C].length && (p[g++] = y[C][v]);
  for (v = 0; v < d; v++)
    for (C = 0; C < o; C++)
      p[g++] = P[C][v];
  return p;
}
function qi(i, t, e, s) {
  let n;
  if (Array.isArray(i))
    n = Ht.fromArray(i);
  else if (typeof i == "string") {
    let l = t;
    if (!l) {
      const h = Ht.rawSplit(i);
      l = St.getBestVersionForData(h, e);
    }
    n = Ht.fromString(i, l || 40);
  } else
    throw new Error("Invalid data");
  const r = St.getBestVersionForData(n, e);
  if (!r)
    throw new Error("The amount of data is too big to be stored in a QR Code");
  if (!t)
    t = r;
  else if (t < r)
    throw new Error(
      `
The chosen QR Code version cannot contain this amount of data.
Minimum version required to store current data is: ` + r + `.
`
    );
  const o = Ki(t, e, n), c = Tt.getSymbolSize(t), a = new Ri(c);
  return Hi(a, t), Fi(a), Vi(a, t), Ft(a, e, 0), t >= 7 && zi(a, t), ji(a, o), isNaN(s) && (s = jt.getBestMask(
    a,
    Ft.bind(null, a, e)
  )), jt.applyMask(s, a), Ft(a, e, s), {
    modules: a,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: s,
    segments: n
  };
}
Se.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let s = Ot.M, n, r;
  return typeof e < "u" && (s = Ot.from(e.errorCorrectionLevel, Ot.M), n = St.from(e.version), r = jt.from(e.maskPattern), e.toSJISFunc && Tt.setToSJISFunction(e.toSJISFunc)), qi(t, n, s, r);
};
var Oe = {}, ee = {};
(function(i) {
  function t(e) {
    if (typeof e == "number" && (e = e.toString()), typeof e != "string")
      throw new Error("Color should be defined as hex string");
    let s = e.slice().replace("#", "").split("");
    if (s.length < 3 || s.length === 5 || s.length > 8)
      throw new Error("Invalid hex color: " + e);
    (s.length === 3 || s.length === 4) && (s = Array.prototype.concat.apply([], s.map(function(r) {
      return [r, r];
    }))), s.length === 6 && s.push("F", "F");
    const n = parseInt(s.join(""), 16);
    return {
      r: n >> 24 & 255,
      g: n >> 16 & 255,
      b: n >> 8 & 255,
      a: n & 255,
      hex: "#" + s.slice(0, 6).join("")
    };
  }
  i.getOptions = function(s) {
    s || (s = {}), s.color || (s.color = {});
    const n = typeof s.margin > "u" || s.margin === null || s.margin < 0 ? 4 : s.margin, r = s.width && s.width >= 21 ? s.width : void 0, o = s.scale || 4;
    return {
      width: r,
      scale: r ? 4 : o,
      margin: n,
      color: {
        dark: t(s.color.dark || "#000000ff"),
        light: t(s.color.light || "#ffffffff")
      },
      type: s.type,
      rendererOpts: s.rendererOpts || {}
    };
  }, i.getScale = function(s, n) {
    return n.width && n.width >= s + n.margin * 2 ? n.width / (s + n.margin * 2) : n.scale;
  }, i.getImageWidth = function(s, n) {
    const r = i.getScale(s, n);
    return Math.floor((s + n.margin * 2) * r);
  }, i.qrToImageData = function(s, n, r) {
    const o = n.modules.size, c = n.modules.data, a = i.getScale(o, r), l = Math.floor((o + r.margin * 2) * a), h = r.margin * a, f = [r.color.light, r.color.dark];
    for (let d = 0; d < l; d++)
      for (let u = 0; u < l; u++) {
        let _ = (d * l + u) * 4, y = r.color.light;
        if (d >= h && u >= h && d < l - h && u < l - h) {
          const P = Math.floor((d - h) / a), m = Math.floor((u - h) / a);
          y = f[c[P * o + m] ? 1 : 0];
        }
        s[_++] = y.r, s[_++] = y.g, s[_++] = y.b, s[_] = y.a;
      }
  };
})(ee);
(function(i) {
  const t = ee;
  function e(n, r, o) {
    n.clearRect(0, 0, r.width, r.height), r.style || (r.style = {}), r.height = o, r.width = o, r.style.height = o + "px", r.style.width = o + "px";
  }
  function s() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  i.render = function(r, o, c) {
    let a = c, l = o;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), o || (l = s()), a = t.getOptions(a);
    const h = t.getImageWidth(r.modules.size, a), f = l.getContext("2d"), d = f.createImageData(h, h);
    return t.qrToImageData(d.data, r, a), e(f, l, h), f.putImageData(d, 0, 0), l;
  }, i.renderToDataURL = function(r, o, c) {
    let a = c;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), a || (a = {});
    const l = i.render(r, o, a), h = a.type || "image/png", f = a.rendererOpts || {};
    return l.toDataURL(h, f.quality);
  };
})(Oe);
var He = {};
const Ji = ee;
function ye(i, t) {
  const e = i.a / 255, s = t + '="' + i.hex + '"';
  return e < 1 ? s + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : s;
}
function Vt(i, t, e) {
  let s = i + t;
  return typeof e < "u" && (s += " " + e), s;
}
function Wi(i, t, e) {
  let s = "", n = 0, r = !1, o = 0;
  for (let c = 0; c < i.length; c++) {
    const a = Math.floor(c % t), l = Math.floor(c / t);
    !a && !r && (r = !0), i[c] ? (o++, c > 0 && a > 0 && i[c - 1] || (s += r ? Vt("M", a + e, 0.5 + l + e) : Vt("m", n, 0), n = 0, r = !1), a + 1 < t && i[c + 1] || (s += Vt("h", o), o = 0)) : n++;
  }
  return s;
}
He.render = function(t, e, s) {
  const n = Ji.getOptions(e), r = t.modules.size, o = t.modules.data, c = r + n.margin * 2, a = n.color.light.a ? "<path " + ye(n.color.light, "fill") + ' d="M0 0h' + c + "v" + c + 'H0z"/>' : "", l = "<path " + ye(n.color.dark, "stroke") + ' d="' + Wi(o, r, n.margin) + '"/>', h = 'viewBox="0 0 ' + c + " " + c + '"', d = '<svg xmlns="http://www.w3.org/2000/svg" ' + (n.width ? 'width="' + n.width + '" height="' + n.width + '" ' : "") + h + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof s == "function" && s(null, d), d;
};
const Yi = ui, Gt = Se, Fe = Oe, Qi = He;
function ie(i, t, e, s, n) {
  const r = [].slice.call(arguments, 1), o = r.length, c = typeof r[o - 1] == "function";
  if (!c && !Yi())
    throw new Error("Callback required as last argument");
  if (c) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (n = e, e = t, t = s = void 0) : o === 3 && (t.getContext && typeof n > "u" ? (n = s, s = void 0) : (n = s, s = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = s = void 0) : o === 2 && !t.getContext && (s = e, e = t, t = void 0), new Promise(function(a, l) {
      try {
        const h = Gt.create(e, s);
        a(i(h, t, s));
      } catch (h) {
        l(h);
      }
    });
  }
  try {
    const a = Gt.create(e, s);
    n(null, i(a, t, s));
  } catch (a) {
    n(a);
  }
}
yt.create = Gt.create;
yt.toCanvas = ie.bind(null, Fe.render);
yt.toDataURL = ie.bind(null, Fe.renderToDataURL);
yt.toString = ie.bind(null, function(i, t, e) {
  return Qi.render(i, e);
});
var Zi = Object.defineProperty, Xi = Object.getOwnPropertyDescriptor, It = (i, t, e, s) => {
  for (var n = s > 1 ? void 0 : s ? Xi(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (n = (s ? o(t, e, n) : o(n)) || n);
  return s && n && Zi(t, e, n), n;
};
let K = class extends T {
  constructor() {
    super(...arguments), this._qrSvg = "";
  }
  setConfig(i) {
    if (!i || !i.ssid)
      throw new Error("Please define an SSID");
    this._config = i;
  }
  static getStubConfig() {
    return {
      ssid: "Guest WiFi",
      password: "password123",
      name: "Wi-Fi Access"
    };
  }
  updated(i) {
    var t, e, s, n;
    if (i.has("hass") || i.has("_config")) {
      const r = i.has("hass") ? this._getValueFromHass((t = this._config) == null ? void 0 : t.ssid, i.get("hass")) : null, o = this._getValue((e = this._config) == null ? void 0 : e.ssid), c = i.has("hass") ? this._getValueFromHass((s = this._config) == null ? void 0 : s.password, i.get("hass")) : null, a = this._getValue((n = this._config) == null ? void 0 : n.password);
      (i.has("_config") || r !== o || c !== a) && this._generateQR();
    }
  }
  _getValueFromHass(i, t) {
    return !i || !t ? i || "" : t.states[i] ? t.states[i].state : i;
  }
  _getValue(i) {
    return !i || !this.hass ? i || "" : this.hass.states[i] ? this.hass.states[i].state : i;
  }
  _generateWifiString(i, t) {
    const e = i.replace(/([\\;,":])/g, "\\$1"), s = t ? t.replace(/([\\;,":])/g, "\\$1") : "";
    return s ? `WIFI:T:WPA;S:${e};P:${s};;` : `WIFI:T:nopass;S:${e};P:;;`;
  }
  async _generateQR() {
    if (!this._config) return;
    const i = this._getValue(this._config.ssid), t = this._getValue(this._config.password);
    if (!i) {
      this._qrSvg = "";
      return;
    }
    const e = this._generateWifiString(i, t);
    try {
      this._qrSvg = await yt.toString(e, {
        type: "svg",
        margin: 2,
        color: {
          dark: "#000000",
          light: "#ffffff"
        }
      });
    } catch (s) {
      console.error("Failed to generate QR code", s), this._qrSvg = "";
    }
  }
  render() {
    if (!this._config || !this.hass)
      return E``;
    const i = this._getValue(this._config.ssid), t = this._getValue(this._config.password);
    return E`
      <ha-card .header="${this._config.name || "Wi-Fi Access"}">
        <div class="card-content">
          <div class="ssid-display">${i}</div>
          <div class="qr-container" .innerHTML="${this._qrSvg}"></div>
          ${t ? E`<div class="password-display">Password: <code>${t}</code></div>` : ""}
        </div>
      </ha-card>
    `;
  }
};
K.styles = G`
    :host {
      display: block;
    }
    .card-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
      gap: 16px;
    }
    .ssid-display {
      font-size: 1.5em;
      font-weight: bold;
      color: var(--primary-text-color);
      text-align: center;
    }
    .qr-container {
      width: 200px;
      height: 200px;
      background: white;
      padding: 8px;
      border-radius: 8px;
    }
    .qr-container svg {
      width: 100%;
      height: 100%;
    }
    .password-display {
      color: var(--secondary-text-color);
      text-align: center;
    }
    code {
      background: var(--secondary-background-color);
      padding: 2px 4px;
      border-radius: 4px;
      font-family: monospace;
    }
  `;
It([
  O({ attribute: !1 })
], K.prototype, "hass", 2);
It([
  b()
], K.prototype, "_config", 2);
It([
  b()
], K.prototype, "_qrSvg", 2);
K = It([
  tt("meraki-wifi-qr-card")
], K);
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", K);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var tn = Object.defineProperty, en = Object.getOwnPropertyDescriptor, it = (i, t, e, s) => {
  for (var n = s > 1 ? void 0 : s ? en(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (n = (s ? o(t, e, n) : o(n)) || n);
  return s && n && tn(t, e, n), n;
};
let gt = class extends T {
  static async getConfigElement() {
    return document.createElement("meraki-network-vitals-card-editor");
  }
  setConfig(i) {
    if (!i)
      throw new Error("Invalid configuration");
    this._config = i;
  }
  static getStubConfig() {
    return {
      gateway_entity: "",
      switch_entity: "",
      ap_entity: "",
      throughput_entity: "",
      name: "Meraki Network Vitals"
    };
  }
  _renderStatusDot(i, t) {
    if (!i || !this.hass.states[i])
      return E`
        <div class="status-item">
          <svg height="12" width="12">
            <circle cx="6" cy="6" r="6" fill="var(--disabled-text-color)" />
          </svg>
          <span class="status-label">${t}</span>
        </div>
      `;
    const e = this.hass.states[i], s = e ? e.state.toLowerCase() : "unknown";
    let n = "var(--disabled-text-color)";
    return s === "ok" || s === "online" || s === "connected" ? n = "var(--success-color)" : s === "warning" ? n = "var(--warning-color)" : (s === "error" || s === "offline" || s === "failed") && (n = "var(--error-color)"), E`
      <div class="status-item">
        <svg height="12" width="12">
          <circle cx="6" cy="6" r="6" fill="${n}" />
        </svg>
        <span class="status-label">${t}</span>
      </div>
    `;
  }
  render() {
    if (!this._config || !this.hass)
      return E``;
    const i = this._config.throughput_entity, t = i && this.hass.states[i] ? this.hass.states[i].state + " " + (this.hass.states[i].attributes.unit_of_measurement || "") : "N/A";
    return E`
      <ha-card>
        <div class="card-content">
          <div class="vitals-container">
            <div class="status-dots">
              ${this._renderStatusDot(this._config.gateway_entity, "Gateway")}
              ${this._renderStatusDot(this._config.switch_entity, "Switches")}
              ${this._renderStatusDot(this._config.ap_entity, "APs")}
            </div>
            <div class="throughput-container">
              <ha-icon icon="mdi:swap-vertical"></ha-icon>
              <span class="throughput-value">${t}</span>
            </div>
          </div>
        </div>
      </ha-card>
    `;
  }
};
gt.styles = G`
    :host {
      display: block;
    }
    .card-content {
      padding: 12px 16px;
    }
    .vitals-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }
    .status-dots {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
    }
    .status-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-right: 16px;
    }
    .status-label {
      font-size: 14px;
      font-weight: 500;
      color: var(--primary-text-color);
      white-space: nowrap;
    }
    .throughput-container {
      display: flex;
      align-items: center;
      gap: 4px;
      color: var(--secondary-text-color);
    }
    .throughput-value {
      font-size: 14px;
      font-weight: 500;
      white-space: nowrap;
    }
    ha-icon {
      --mdc-icon-size: 18px;
    }
  `;
it([
  O({ attribute: !1 })
], gt.prototype, "hass", 2);
it([
  b()
], gt.prototype, "_config", 2);
gt = it([
  tt("meraki-network-vitals-card")
], gt);
let pt = class extends T {
  setConfig(i) {
    this._config = i;
  }
  render() {
    return !this.hass || !this._config ? E`` : E`
      <div class="card-config">
        <ha-textfield
          label="Name (Optional)"
          .value="${this._config.name || ""}"
          .configValue="${"name"}"
          @input="${this._valueChanged}"
          style="width: 100%; margin-bottom: 16px;"
        ></ha-textfield>
        <ha-entity-picker
          label="Gateway Entity"
          .hass="${this.hass}"
          .value="${this._config.gateway_entity || ""}"
          .configValue="${"gateway_entity"}"
          @value-changed="${this._valueChanged}"
          allow-custom-entity
          style="width: 100%; margin-bottom: 16px; display: block;"
        ></ha-entity-picker>
        <ha-entity-picker
          label="Switch Entity"
          .hass="${this.hass}"
          .value="${this._config.switch_entity || ""}"
          .configValue="${"switch_entity"}"
          @value-changed="${this._valueChanged}"
          allow-custom-entity
          style="width: 100%; margin-bottom: 16px; display: block;"
        ></ha-entity-picker>
        <ha-entity-picker
          label="AP Entity"
          .hass="${this.hass}"
          .value="${this._config.ap_entity || ""}"
          .configValue="${"ap_entity"}"
          @value-changed="${this._valueChanged}"
          allow-custom-entity
          style="width: 100%; margin-bottom: 16px; display: block;"
        ></ha-entity-picker>
        <ha-entity-picker
          label="Throughput Entity"
          .hass="${this.hass}"
          .value="${this._config.throughput_entity || ""}"
          .configValue="${"throughput_entity"}"
          @value-changed="${this._valueChanged}"
          allow-custom-entity
          style="width: 100%; display: block;"
        ></ha-entity-picker>
      </div>
    `;
  }
  _valueChanged(i) {
    if (!this._config || !this.hass) return;
    const t = i.target, e = t.value, s = t.configValue;
    if (this._config[s] === e) return;
    const n = {
      ...this._config,
      [s]: e
    }, r = new CustomEvent("config-changed", {
      detail: { config: n },
      bubbles: !0,
      composed: !0
    });
    this.dispatchEvent(r);
  }
};
pt.styles = G`
    .card-config {
      display: flex;
      flex-direction: column;
    }
  `;
it([
  O({ attribute: !1 })
], pt.prototype, "hass", 2);
it([
  b()
], pt.prototype, "_config", 2);
pt = it([
  tt("meraki-network-vitals-card-editor")
], pt);
window.customCards = window.customCards || [];
window.customCards.some((i) => i.type === "meraki-network-vitals-card") || window.customCards.push({
  type: "meraki-network-vitals-card",
  name: "Meraki Network Vitals",
  description: "Compact horizontal header for Meraki network health and throughput.",
  preview: !0
});
var nn = Object.defineProperty, sn = Object.getOwnPropertyDescriptor, ne = (i, t, e, s) => {
  for (var n = s > 1 ? void 0 : s ? sn(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (n = (s ? o(t, e, n) : o(n)) || n);
  return s && n && nn(t, e, n), n;
};
let _t = class extends T {
  setConfig(i) {
    this._config = i;
  }
  render() {
    return !this.hass || !this._config ? E`` : E`
      <div class="card-config">
        <ha-textfield
          label="Name (Optional)"
          .value="${this._config.name || ""}"
          .configValue="${"name"}"
          @input="${this._valueChanged}"
          style="width: 100%; margin-bottom: 16px;"
        ></ha-textfield>
      </div>
    `;
  }
  _valueChanged(i) {
    if (!this._config || !this.hass) return;
    const t = i.target, e = t.value, s = t.configValue;
    if (this._config[s] === e) return;
    const n = {
      ...this._config,
      [s]: e
    };
    (n[s] === "" || n[s] === void 0) && delete n[s];
    const r = new CustomEvent("config-changed", {
      detail: { config: n },
      bubbles: !0,
      composed: !0
    });
    this.dispatchEvent(r);
  }
};
_t.styles = G`
    .card-config {
      display: flex;
      flex-direction: column;
    }
  `;
ne([
  O({ attribute: !1 })
], _t.prototype, "hass", 2);
ne([
  b()
], _t.prototype, "_config", 2);
_t = ne([
  tt("meraki-guest-access-card-editor")
], _t);
var qt = /* @__PURE__ */ ((i) => (i.GET_CONFIG = "meraki_ha/get_config", i.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", i.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", i.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", i.GET_VERSION = "meraki_ha/get_version", i.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", i.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", i.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", i.GET_GUEST_KEYS = "meraki_ha/ipsk/get", i.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", i.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", i))(qt || {});
const we = async (i, t) => {
  if (!i)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof i.callWS == "function")
      return await i.callWS(t);
    if (i.connection && typeof i.connection.sendMessagePromise == "function")
      return await i.connection.sendMessagePromise(t);
    throw new Error("Home Assistant WebSocket communication methods not found.");
  } catch (e) {
    throw console.error(`Meraki HA: WebSocket error [${t.type}]:`, e), e;
  }
};
var rn = Object.defineProperty, k = (i, t, e, s) => {
  for (var n = void 0, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (n = o(t, e, n) || n);
  return n && rn(t, e, n), n;
};
const se = class se extends T {
  constructor() {
    super(...arguments), this._selectedNetwork = "", this._selectedSSID = "", this._selectedPolicy = "", this._selectedDuration = "60", this._customName = "", this._customPassphrase = "", this._creating = !1, this._error = null, this._success = null, this._networks = [], this._ssids = [], this._policies = [], this._loading = !0, this._initDone = !1;
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = t;
  }
  static async getConfigElement() {
    return document.createElement("meraki-guest-access-card-editor");
  }
  static getStubConfig() {
    return {
      name: "Meraki Guest Access"
    };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._fetchInitialData();
  }
  updated(t) {
    var e;
    super.updated(t), t.has("hass") && this.hass && (!this._initDone && this.hass && this._fetchInitialData(), (e = this.hass.user) != null && e.name && !this._customName && (this._customName = this.hass.user.name));
  }
  async _fetchInitialData() {
    var t;
    if (this._initDone = !0, !!this.hass) {
      this._loading = !0;
      try {
        const e = await this.hass.callWS({
          type: "config_entries/get",
          domain: "meraki_ha"
        }), s = ((t = this._config) == null ? void 0 : t.config_entry_id) || (e.length > 0 ? e[0].entry_id : null);
        if (!s) {
          this._error = "Meraki integration not found. Please configure it first.", this._loading = !1;
          return;
        }
        const n = await we(this.hass, {
          type: qt.GET_CONFIG,
          config_entry_id: s
        });
        this._networks = (Array.isArray(n.networks) ? n.networks : []).filter((r) => {
          var o;
          return (o = r.productTypes) == null ? void 0 : o.includes("wireless");
        }), this._ssids = Array.isArray(n.ssids) ? n.ssids : [], this._networks.length > 0 && !this._selectedNetwork && (this._selectedNetwork = this._networks[0].id, this._fetchPolicies(this._selectedNetwork, s));
      } catch (e) {
        this._error = `Failed to fetch Meraki data: ${e.message || e}`;
      } finally {
        this._loading = !1;
      }
    }
  }
  async _fetchSSIDs() {
  }
  async _fetchPolicies(t, e) {
    var s;
    if (this.hass)
      try {
        let n = e || ((s = this._config) == null ? void 0 : s.config_entry_id);
        if (!n) {
          const o = await this.hass.callWS({
            type: "config_entries/get",
            domain: "meraki_ha"
          });
          n = o.length > 0 ? o[0].entry_id : void 0;
        }
        if (!n) return;
        const r = await we(this.hass, {
          type: qt.TIMED_ACCESS_GET_POLICIES,
          config_entry_id: n,
          network_id: t
        });
        this._policies = Array.isArray(r) ? r : (r == null ? void 0 : r.policies) || [];
      } catch (n) {
        console.error("Failed to fetch policies:", n), this._policies = [];
      }
  }
  render() {
    var e, s;
    if (this._loading && !this._networks.length)
      return E`
        <ha-card .header="${((e = this._config) == null ? void 0 : e.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    const t = (this._ssids || []).filter((n) => n.networkId === this._selectedNetwork);
    return E`
      <ha-card .header="${((s = this._config) == null ? void 0 : s.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? E`
                <ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => this._error = null}">
                  ${this._error}
                </ha-alert>
              ` : ""}
          ${this._success ? E`
                <ha-alert alert-type="success" dismissable @alert-dismissed-clicked="${() => this._success = null}">
                  ${this._success}
                </ha-alert>
              ` : ""}

          <div class="form-container">
            <ha-select
              label="Network"
              value="${this._selectedNetwork}"
              @closed="${this._handleNetworkChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(this._networks || []).map(
      (n) => E`
                  <mwc-list-item value="${n.id}">
                    ${n.name}
                  </mwc-list-item>
                `
    )}
            </ha-select>

            <ha-select
              label="SSID"
              value="${this._selectedSSID}"
              .disabled="${!this._selectedNetwork}"
              @closed="${this._handleSSIDChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(t || []).map(
      (n) => E`
                  <mwc-list-item value="${String(n.number)}">
                    ${n.name} (SSID ${n.number})
                  </mwc-list-item>
                `
    )}
            </ha-select>

            <ha-select
              label="Group Policy"
              value="${this._selectedPolicy}"
              .disabled="${!this._selectedNetwork}"
              @closed="${this._handlePolicyChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <mwc-list-item value="">None (Default)</mwc-list-item>
              ${(this._policies || []).map(
      (n) => E`
                  <mwc-list-item value="${String(n.groupPolicyId)}">
                    ${n.name}
                  </mwc-list-item>
                `
    )}
            </ha-select>

            <ha-select
              label="Duration"
              value="${this._selectedDuration}"
              @closed="${this._handleDurationChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <mwc-list-item value="30">30 Minutes</mwc-list-item>
              <mwc-list-item value="60">1 Hour</mwc-list-item>
              <mwc-list-item value="240">4 Hours</mwc-list-item>
              <mwc-list-item value="1440">24 Hours</mwc-list-item>
              <mwc-list-item value="10080">7 Days</mwc-list-item>
            </ha-select>

            <ha-textfield
              label="Name (Optional)"
              placeholder="e.g. Guest-John"
              .value="${this._customName}"
              @input="${(n) => this._customName = n.target.value}"
            ></ha-textfield>

            <ha-textfield
              label="Passphrase (Optional)"
              placeholder="Leave empty to auto-generate"
              .value="${this._customPassphrase}"
              @input="${(n) => this._customPassphrase = n.target.value}"
            ></ha-textfield>

            <ha-button
              raised
              .disabled="${this._creating || !this._selectedNetwork || !this._selectedSSID}"
              @click="${this._handleCreate}"
            >
              ${this._creating ? "Creating..." : "Generate access key"}
            </ha-button>
          </div>
        </div>
      </ha-card>
    `;
  }
  _handleNetworkChange(t) {
    t.stopPropagation();
    const s = t.target.value;
    !s || s === this._selectedNetwork || (this._selectedNetwork = s, this._selectedSSID = "", this._selectedPolicy = "", this._fetchSSIDs(), this._fetchPolicies(s));
  }
  _handleSSIDChange(t) {
    t.stopPropagation();
    const e = t.target;
    this._selectedSSID = e.value;
  }
  _handlePolicyChange(t) {
    t.stopPropagation();
    const e = t.target;
    this._selectedPolicy = e.value;
  }
  _handleDurationChange(t) {
    t.stopPropagation();
    const e = t.target;
    this._selectedDuration = e.value;
  }
  async _handleCreate() {
    if (!(!this._selectedNetwork || !this._selectedSSID)) {
      this._creating = !0, this._error = null, this._success = null;
      try {
        await this.hass.callService("meraki_ha", "create_guest_key", {
          network_id: this._selectedNetwork,
          ssid_number: parseInt(this._selectedSSID, 10),
          duration_minutes: parseInt(this._selectedDuration, 10),
          name: this._customName || void 0,
          passphrase: this._customPassphrase || void 0,
          group_policy_id: this._selectedPolicy || void 0
        }), this._success = "Guest access key created successfully!", this._customName = "", this._customPassphrase = "";
      } catch (t) {
        this._error = `Failed to create guest key: ${t.message || t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
se.styles = G`
    :host {
      display: block;
    }
    .card-content {
      padding: 16px;
    }
    .form-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    ha-select, ha-textfield, ha-button {
      width: 100%;
    }
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    .flex {
      display: flex;
    }
    .justify-center {
      justify-content: center;
    }
    .p-8 {
      padding: 32px;
    }
  `;
let A = se;
k([
  O({ attribute: !1 })
], A.prototype, "hass");
k([
  b()
], A.prototype, "_config");
k([
  b()
], A.prototype, "_selectedNetwork");
k([
  b()
], A.prototype, "_selectedSSID");
k([
  b()
], A.prototype, "_selectedPolicy");
k([
  b()
], A.prototype, "_selectedDuration");
k([
  b()
], A.prototype, "_customName");
k([
  b()
], A.prototype, "_customPassphrase");
k([
  b()
], A.prototype, "_creating");
k([
  b()
], A.prototype, "_error");
k([
  b()
], A.prototype, "_success");
k([
  b()
], A.prototype, "_networks");
k([
  b()
], A.prototype, "_ssids");
k([
  b()
], A.prototype, "_policies");
k([
  b()
], A.prototype, "_loading");
k([
  b()
], A.prototype, "_initDone");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", A);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: !0
});
export {
  A as MerakiGuestAccessCard
};
