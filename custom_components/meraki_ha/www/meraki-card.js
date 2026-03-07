/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const wt = globalThis, Gt = wt.ShadowRoot && (wt.ShadyCSS === void 0 || wt.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Kt = Symbol(), se = /* @__PURE__ */ new WeakMap();
let we = class {
  constructor(t, e, n) {
    if (this._$cssResult$ = !0, n !== Kt) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Gt && t === void 0) {
      const n = e !== void 0 && e.length === 1;
      n && (t = se.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), n && se.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const Oe = (i) => new we(typeof i == "string" ? i : i + "", void 0, Kt), dt = (i, ...t) => {
  const e = i.length === 1 ? i[0] : t.reduce((n, s, r) => n + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(s) + i[r + 1], i[0]);
  return new we(e, i, Kt);
}, He = (i, t) => {
  if (Gt) i.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const n = document.createElement("style"), s = wt.litNonce;
    s !== void 0 && n.setAttribute("nonce", s), n.textContent = e.cssText, i.appendChild(n);
  }
}, ne = Gt ? (i) => i : (i) => i instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const n of t.cssRules) e += n.cssText;
  return Oe(e);
})(i) : i;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: Fe, defineProperty: Ve, getOwnPropertyDescriptor: ze, getOwnPropertyNames: je, getOwnPropertySymbols: Ge, getPrototypeOf: Ke } = Object, H = globalThis, re = H.trustedTypes, qe = re ? re.emptyScript : "", It = H.reactiveElementPolyfillSupport, st = (i, t) => i, yt = { toAttribute(i, t) {
  switch (t) {
    case Boolean:
      i = i ? qe : null;
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
} }, qt = (i, t) => !Fe(i, t), oe = { attribute: !0, type: String, converter: yt, reflect: !1, useDefault: !1, hasChanged: qt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), H.litPropertyMetadata ?? (H.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let q = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = oe) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const n = Symbol(), s = this.getPropertyDescriptor(t, n, e);
      s !== void 0 && Ve(this.prototype, t, s);
    }
  }
  static getPropertyDescriptor(t, e, n) {
    const { get: s, set: r } = ze(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: s, set(o) {
      const c = s == null ? void 0 : s.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, c, n);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? oe;
  }
  static _$Ei() {
    if (this.hasOwnProperty(st("elementProperties"))) return;
    const t = Ke(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(st("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(st("properties"))) {
      const e = this.properties, n = [...je(e), ...Ge(e)];
      for (const s of n) this.createProperty(s, e[s]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [n, s] of e) this.elementProperties.set(n, s);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, n] of this.elementProperties) {
      const s = this._$Eu(e, n);
      s !== void 0 && this._$Eh.set(s, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const n = new Set(t.flat(1 / 0).reverse());
      for (const s of n) e.unshift(ne(s));
    } else t !== void 0 && e.push(ne(t));
    return e;
  }
  static _$Eu(t, e) {
    const n = e.attribute;
    return n === !1 ? void 0 : typeof n == "string" ? n : typeof t == "string" ? t.toLowerCase() : void 0;
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
    for (const n of e.keys()) this.hasOwnProperty(n) && (t.set(n, this[n]), delete this[n]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return He(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    var t;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$EO) == null || t.forEach((e) => {
      var n;
      return (n = e.hostConnected) == null ? void 0 : n.call(e);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$EO) == null || t.forEach((e) => {
      var n;
      return (n = e.hostDisconnected) == null ? void 0 : n.call(e);
    });
  }
  attributeChangedCallback(t, e, n) {
    this._$AK(t, n);
  }
  _$ET(t, e) {
    var r;
    const n = this.constructor.elementProperties.get(t), s = this.constructor._$Eu(t, n);
    if (s !== void 0 && n.reflect === !0) {
      const o = (((r = n.converter) == null ? void 0 : r.toAttribute) !== void 0 ? n.converter : yt).toAttribute(e, n.type);
      this._$Em = t, o == null ? this.removeAttribute(s) : this.setAttribute(s, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const n = this.constructor, s = n._$Eh.get(t);
    if (s !== void 0 && this._$Em !== s) {
      const c = n.getPropertyOptions(s), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((r = c.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? c.converter : yt;
      this._$Em = s;
      const l = a.fromAttribute(e, c.type);
      this[s] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(s)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, n, s = !1, r) {
    var o;
    if (t !== void 0) {
      const c = this.constructor;
      if (s === !1 && (r = this[t]), n ?? (n = c.getPropertyOptions(t)), !((n.hasChanged ?? qt)(r, e) || n.useDefault && n.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(c._$Eu(t, n)))) return;
      this.C(t, e, n);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: n, reflect: s, wrapped: r }, o) {
    n && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || n || (e = void 0), this._$AL.set(t, e)), s === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
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
    var n;
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this._$Ep) {
        for (const [r, o] of this._$Ep) this[r] = o;
        this._$Ep = void 0;
      }
      const s = this.constructor.elementProperties;
      if (s.size > 0) for (const [r, o] of s) {
        const { wrapped: c } = o, a = this[r];
        c !== !0 || this._$AL.has(r) || a === void 0 || this.C(r, void 0, o, a);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (n = this._$EO) == null || n.forEach((s) => {
        var r;
        return (r = s.hostUpdate) == null ? void 0 : r.call(s);
      }), this.update(e)) : this._$EM();
    } catch (s) {
      throw t = !1, this._$EM(), s;
    }
    t && this._$AE(e);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var e;
    (e = this._$EO) == null || e.forEach((n) => {
      var s;
      return (s = n.hostUpdated) == null ? void 0 : s.call(n);
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
q.elementStyles = [], q.shadowRootOptions = { mode: "open" }, q[st("elementProperties")] = /* @__PURE__ */ new Map(), q[st("finalized")] = /* @__PURE__ */ new Map(), It == null || It({ ReactiveElement: q }), (H.reactiveElementVersions ?? (H.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const nt = globalThis, ae = (i) => i, Et = nt.trustedTypes, ce = Et ? Et.createPolicy("lit-html", { createHTML: (i) => i }) : void 0, ye = "$lit$", L = `lit$${Math.random().toFixed(9).slice(2)}$`, Ee = "?" + L, We = `<${Ee}>`, G = document, ot = () => G.createComment(""), at = (i) => i === null || typeof i != "object" && typeof i != "function", Wt = Array.isArray, Je = (i) => Wt(i) || typeof (i == null ? void 0 : i[Symbol.iterator]) == "function", Tt = `[
\f\r]`, it = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, le = /-->/g, he = />/g, V = RegExp(`>|${Tt}(?:([^\\s"'>=/]+)(${Tt}*=${Tt}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), ue = /'/g, de = /"/g, ve = /^(?:script|style|textarea|title)$/i, Ye = (i) => (t, ...e) => ({ _$litType$: i, strings: t, values: e }), A = Ye(1), W = Symbol.for("lit-noChange"), $ = Symbol.for("lit-nothing"), fe = /* @__PURE__ */ new WeakMap(), z = G.createTreeWalker(G, 129);
function Se(i, t) {
  if (!Wt(i) || !i.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ce !== void 0 ? ce.createHTML(t) : t;
}
const Qe = (i, t) => {
  const e = i.length - 1, n = [];
  let s, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = it;
  for (let c = 0; c < e; c++) {
    const a = i[c];
    let l, h, f = -1, d = 0;
    for (; d < a.length && (o.lastIndex = d, h = o.exec(a), h !== null); ) d = o.lastIndex, o === it ? h[1] === "!--" ? o = le : h[1] !== void 0 ? o = he : h[2] !== void 0 ? (ve.test(h[2]) && (s = RegExp("</" + h[2], "g")), o = V) : h[3] !== void 0 && (o = V) : o === V ? h[0] === ">" ? (o = s ?? it, f = -1) : h[1] === void 0 ? f = -2 : (f = o.lastIndex - h[2].length, l = h[1], o = h[3] === void 0 ? V : h[3] === '"' ? de : ue) : o === de || o === ue ? o = V : o === le || o === he ? o = it : (o = V, s = void 0);
    const u = o === V && i[c + 1].startsWith("/>") ? " " : "";
    r += o === it ? a + We : f >= 0 ? (n.push(l), a.slice(0, f) + ye + a.slice(f) + L + u) : a + L + (f === -2 ? c : u);
  }
  return [Se(i, r + (i[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), n];
};
class ct {
  constructor({ strings: t, _$litType$: e }, n) {
    let s;
    this.parts = [];
    let r = 0, o = 0;
    const c = t.length - 1, a = this.parts, [l, h] = Qe(t, e);
    if (this.el = ct.createElement(l, n), z.currentNode = this.el.content, e === 2 || e === 3) {
      const f = this.el.content.firstChild;
      f.replaceWith(...f.childNodes);
    }
    for (; (s = z.nextNode()) !== null && a.length < c; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) for (const f of s.getAttributeNames()) if (f.endsWith(ye)) {
          const d = h[o++], u = s.getAttribute(f).split(L), _ = /([.?@])?(.*)/.exec(d);
          a.push({ type: 1, index: r, name: _[2], strings: u, ctor: _[1] === "." ? Xe : _[1] === "?" ? ti : _[1] === "@" ? ei : Ct }), s.removeAttribute(f);
        } else f.startsWith(L) && (a.push({ type: 6, index: r }), s.removeAttribute(f));
        if (ve.test(s.tagName)) {
          const f = s.textContent.split(L), d = f.length - 1;
          if (d > 0) {
            s.textContent = Et ? Et.emptyScript : "";
            for (let u = 0; u < d; u++) s.append(f[u], ot()), z.nextNode(), a.push({ type: 2, index: ++r });
            s.append(f[d], ot());
          }
        }
      } else if (s.nodeType === 8) if (s.data === Ee) a.push({ type: 2, index: r });
      else {
        let f = -1;
        for (; (f = s.data.indexOf(L, f + 1)) !== -1; ) a.push({ type: 7, index: r }), f += L.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const n = G.createElement("template");
    return n.innerHTML = t, n;
  }
}
function J(i, t, e = i, n) {
  var o, c;
  if (t === W) return t;
  let s = n !== void 0 ? (o = e._$Co) == null ? void 0 : o[n] : e._$Cl;
  const r = at(t) ? void 0 : t._$litDirective$;
  return (s == null ? void 0 : s.constructor) !== r && ((c = s == null ? void 0 : s._$AO) == null || c.call(s, !1), r === void 0 ? s = void 0 : (s = new r(i), s._$AT(i, e, n)), n !== void 0 ? (e._$Co ?? (e._$Co = []))[n] = s : e._$Cl = s), s !== void 0 && (t = J(i, s._$AS(i, t.values), s, n)), t;
}
class Ze {
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
    const { el: { content: e }, parts: n } = this._$AD, s = ((t == null ? void 0 : t.creationScope) ?? G).importNode(e, !0);
    z.currentNode = s;
    let r = z.nextNode(), o = 0, c = 0, a = n[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let l;
        a.type === 2 ? l = new ft(r, r.nextSibling, this, t) : a.type === 1 ? l = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (l = new ii(r, this, t)), this._$AV.push(l), a = n[++c];
      }
      o !== (a == null ? void 0 : a.index) && (r = z.nextNode(), o++);
    }
    return z.currentNode = G, s;
  }
  p(t) {
    let e = 0;
    for (const n of this._$AV) n !== void 0 && (n.strings !== void 0 ? (n._$AI(t, n, e), e += n.strings.length - 2) : n._$AI(t[e])), e++;
  }
}
class ft {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, n, s) {
    this.type = 2, this._$AH = $, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = n, this.options = s, this._$Cv = (s == null ? void 0 : s.isConnected) ?? !0;
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
    t = J(this, t, e), at(t) ? t === $ || t == null || t === "" ? (this._$AH !== $ && this._$AR(), this._$AH = $) : t !== this._$AH && t !== W && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : Je(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== $ && at(this._$AH) ? this._$AA.nextSibling.data = t : this.T(G.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: n } = t, s = typeof n == "number" ? this._$AC(t) : (n.el === void 0 && (n.el = ct.createElement(Se(n.h, n.h[0]), this.options)), n);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === s) this._$AH.p(e);
    else {
      const o = new Ze(s, this), c = o.u(this.options);
      o.p(e), this.T(c), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = fe.get(t.strings);
    return e === void 0 && fe.set(t.strings, e = new ct(t)), e;
  }
  k(t) {
    Wt(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let n, s = 0;
    for (const r of t) s === e.length ? e.push(n = new ft(this.O(ot()), this.O(ot()), this, this.options)) : n = e[s], n._$AI(r), s++;
    s < e.length && (this._$AR(n && n._$AB.nextSibling, s), e.length = s);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var n;
    for ((n = this._$AP) == null ? void 0 : n.call(this, !1, !0, e); t !== this._$AB; ) {
      const s = ae(t).nextSibling;
      ae(t).remove(), t = s;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class Ct {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, n, s, r) {
    this.type = 1, this._$AH = $, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = r, n.length > 2 || n[0] !== "" || n[1] !== "" ? (this._$AH = Array(n.length - 1).fill(new String()), this.strings = n) : this._$AH = $;
  }
  _$AI(t, e = this, n, s) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = J(this, t, e, 0), o = !at(t) || t !== this._$AH && t !== W, o && (this._$AH = t);
    else {
      const c = t;
      let a, l;
      for (t = r[0], a = 0; a < r.length - 1; a++) l = J(this, c[n + a], e, a), l === W && (l = this._$AH[a]), o || (o = !at(l) || l !== this._$AH[a]), l === $ ? t = $ : t !== $ && (t += (l ?? "") + r[a + 1]), this._$AH[a] = l;
    }
    o && !s && this.j(t);
  }
  j(t) {
    t === $ ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class Xe extends Ct {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === $ ? void 0 : t;
  }
}
class ti extends Ct {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== $);
  }
}
class ei extends Ct {
  constructor(t, e, n, s, r) {
    super(t, e, n, s, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = J(this, t, e, 0) ?? $) === W) return;
    const n = this._$AH, s = t === $ && n !== $ || t.capture !== n.capture || t.once !== n.once || t.passive !== n.passive, r = t !== $ && (n === $ || s);
    s && this.element.removeEventListener(this.name, this, n), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class ii {
  constructor(t, e, n) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = n;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    J(this, t);
  }
}
const Bt = nt.litHtmlPolyfillSupport;
Bt == null || Bt(ct, ft), (nt.litHtmlVersions ?? (nt.litHtmlVersions = [])).push("3.3.2");
const si = (i, t, e) => {
  const n = (e == null ? void 0 : e.renderBefore) ?? t;
  let s = n._$litPart$;
  if (s === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    n._$litPart$ = s = new ft(t.insertBefore(ot(), r), r, void 0, e ?? {});
  }
  return s._$AI(i), s;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const j = globalThis;
class R extends q {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = si(e, this.renderRoot, this.renderOptions);
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
    return W;
  }
}
var me;
R._$litElement$ = !0, R.finalized = !0, (me = j.litElementHydrateSupport) == null || me.call(j, { LitElement: R });
const Dt = j.litElementPolyfillSupport;
Dt == null || Dt({ LitElement: R });
(j.litElementVersions ?? (j.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const bt = (i) => (t, e) => {
  e !== void 0 ? e.addInitializer(() => {
    customElements.define(i, t);
  }) : customElements.define(i, t);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ni = { attribute: !0, type: String, converter: yt, reflect: !1, hasChanged: qt }, ri = (i = ni, t, e) => {
  const { kind: n, metadata: s } = e;
  let r = globalThis.litPropertyMetadata.get(s);
  if (r === void 0 && globalThis.litPropertyMetadata.set(s, r = /* @__PURE__ */ new Map()), n === "setter" && ((i = Object.create(i)).wrapped = !0), r.set(e.name, i), n === "accessor") {
    const { name: o } = e;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(o, a, i, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(o, void 0, i, c), c;
    } };
  }
  if (n === "setter") {
    const { name: o } = e;
    return function(c) {
      const a = this[o];
      t.call(this, c), this.requestUpdate(o, a, i, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + n);
};
function tt(i) {
  return (t, e) => typeof e == "object" ? ri(i, t, e) : ((n, s, r) => {
    const o = s.hasOwnProperty(r);
    return s.constructor.createProperty(r, n), o ? Object.getOwnPropertyDescriptor(s, r) : void 0;
  })(i, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function v(i) {
  return tt({ ...i, state: !0, attribute: !1 });
}
var oi = Object.defineProperty, ai = Object.getOwnPropertyDescriptor, Jt = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? ai(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && oi(t, e, s), s;
};
let lt = class extends R {
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
      return A``;
    const i = this._config.entity, t = this.hass.states[i];
    if (!t)
      return A`
        <ha-card>
          <div class="card-content">
            <ha-alert alert-type="error">Entity not found: ${i}</ha-alert>
          </div>
        </ha-card>
      `;
    const e = t.state, n = t.attributes.options || ["None", "Security", "Family", "Strict"], s = this._config.name || t.attributes.friendly_name || "Content Filter";
    return A`
      <ha-card>
        <div class="card-header">${s}</div>
        <div class="card-content">
          <div class="current-profile">
            Current Profile: <strong>${e}</strong>
          </div>
          <div class="profile-buttons">
            ${n.map((r) => A`
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
lt.styles = dt`
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
Jt([
  tt({ attribute: !1 })
], lt.prototype, "hass", 2);
Jt([
  v()
], lt.prototype, "_config", 2);
lt = Jt([
  bt("meraki-content-filter-card")
], lt);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var vt = /* @__PURE__ */ ((i) => (i.GET_CONFIG = "meraki_ha/get_config", i.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", i.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", i.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", i.GET_VERSION = "meraki_ha/get_version", i.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", i.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", i.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", i.GET_GUEST_KEYS = "meraki_ha/ipsk/get", i.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", i.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", i))(vt || {});
const Ht = async (i, t) => {
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
var gt = {}, ci = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, Ae = {}, N = {};
let Yt;
const li = [
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
  return li[t];
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
  Yt = t;
};
N.isKanjiModeEnabled = function() {
  return typeof Yt < "u";
};
N.toSJIS = function(t) {
  return Yt(t);
};
var $t = {};
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
  i.isValid = function(n) {
    return n && typeof n.bit < "u" && n.bit >= 0 && n.bit < 4;
  }, i.from = function(n, s) {
    if (i.isValid(n))
      return n;
    try {
      return t(n);
    } catch {
      return s;
    }
  };
})($t);
function Ce() {
  this.buffer = [], this.length = 0;
}
Ce.prototype = {
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
var hi = Ce;
function pt(i) {
  if (!i || i < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = i, this.data = new Uint8Array(i * i), this.reservedBit = new Uint8Array(i * i);
}
pt.prototype.set = function(i, t, e, n) {
  const s = i * this.size + t;
  this.data[s] = e, n && (this.reservedBit[s] = !0);
};
pt.prototype.get = function(i, t) {
  return this.data[i * this.size + t];
};
pt.prototype.xor = function(i, t, e) {
  this.data[i * this.size + t] ^= e;
};
pt.prototype.isReserved = function(i, t) {
  return this.reservedBit[i * this.size + t];
};
var ui = pt, be = {};
(function(i) {
  const t = N.getSymbolSize;
  i.getRowColCoords = function(n) {
    if (n === 1) return [];
    const s = Math.floor(n / 7) + 2, r = t(n), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * s - 2)) * 2, c = [r - 7];
    for (let a = 1; a < s - 1; a++)
      c[a] = c[a - 1] - o;
    return c.push(6), c.reverse();
  }, i.getPositions = function(n) {
    const s = [], r = i.getRowColCoords(n), o = r.length;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        c === 0 && a === 0 || // top-left
        c === 0 && a === o - 1 || // bottom-left
        c === o - 1 && a === 0 || s.push([r[c], r[a]]);
    return s;
  };
})(be);
var $e = {};
const di = N.getSymbolSize, ge = 7;
$e.getPositions = function(t) {
  const e = di(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - ge, 0],
    // bottom-left
    [0, e - ge]
  ];
};
var Pe = {};
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
  i.isValid = function(s) {
    return s != null && s !== "" && !isNaN(s) && s >= 0 && s <= 7;
  }, i.from = function(s) {
    return i.isValid(s) ? parseInt(s, 10) : void 0;
  }, i.getPenaltyN1 = function(s) {
    const r = s.size;
    let o = 0, c = 0, a = 0, l = null, h = null;
    for (let f = 0; f < r; f++) {
      c = a = 0, l = h = null;
      for (let d = 0; d < r; d++) {
        let u = s.get(f, d);
        u === l ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), l = u, c = 1), u = s.get(d, f), u === h ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), h = u, a = 1);
      }
      c >= 5 && (o += t.N1 + (c - 5)), a >= 5 && (o += t.N1 + (a - 5));
    }
    return o;
  }, i.getPenaltyN2 = function(s) {
    const r = s.size;
    let o = 0;
    for (let c = 0; c < r - 1; c++)
      for (let a = 0; a < r - 1; a++) {
        const l = s.get(c, a) + s.get(c, a + 1) + s.get(c + 1, a) + s.get(c + 1, a + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, i.getPenaltyN3 = function(s) {
    const r = s.size;
    let o = 0, c = 0, a = 0;
    for (let l = 0; l < r; l++) {
      c = a = 0;
      for (let h = 0; h < r; h++)
        c = c << 1 & 2047 | s.get(l, h), h >= 10 && (c === 1488 || c === 93) && o++, a = a << 1 & 2047 | s.get(h, l), h >= 10 && (a === 1488 || a === 93) && o++;
    }
    return o * t.N3;
  }, i.getPenaltyN4 = function(s) {
    let r = 0;
    const o = s.data.length;
    for (let a = 0; a < o; a++) r += s.data[a];
    return Math.abs(Math.ceil(r * 100 / o / 5) - 10) * t.N4;
  };
  function e(n, s, r) {
    switch (n) {
      case i.Patterns.PATTERN000:
        return (s + r) % 2 === 0;
      case i.Patterns.PATTERN001:
        return s % 2 === 0;
      case i.Patterns.PATTERN010:
        return r % 3 === 0;
      case i.Patterns.PATTERN011:
        return (s + r) % 3 === 0;
      case i.Patterns.PATTERN100:
        return (Math.floor(s / 2) + Math.floor(r / 3)) % 2 === 0;
      case i.Patterns.PATTERN101:
        return s * r % 2 + s * r % 3 === 0;
      case i.Patterns.PATTERN110:
        return (s * r % 2 + s * r % 3) % 2 === 0;
      case i.Patterns.PATTERN111:
        return (s * r % 3 + (s + r) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + n);
    }
  }
  i.applyMask = function(s, r) {
    const o = r.size;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        r.isReserved(a, c) || r.xor(a, c, e(s, a, c));
  }, i.getBestMask = function(s, r) {
    const o = Object.keys(i.Patterns).length;
    let c = 0, a = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), i.applyMask(l, s);
      const h = i.getPenaltyN1(s) + i.getPenaltyN2(s) + i.getPenaltyN3(s) + i.getPenaltyN4(s);
      i.applyMask(l, s), h < a && (a = h, c = l);
    }
    return c;
  };
})(Pe);
var Pt = {};
const O = $t, _t = [
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
], mt = [
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
Pt.getBlocksCount = function(t, e) {
  switch (e) {
    case O.L:
      return _t[(t - 1) * 4 + 0];
    case O.M:
      return _t[(t - 1) * 4 + 1];
    case O.Q:
      return _t[(t - 1) * 4 + 2];
    case O.H:
      return _t[(t - 1) * 4 + 3];
    default:
      return;
  }
};
Pt.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case O.L:
      return mt[(t - 1) * 4 + 0];
    case O.M:
      return mt[(t - 1) * 4 + 1];
    case O.Q:
      return mt[(t - 1) * 4 + 2];
    case O.H:
      return mt[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var ke = {}, kt = {};
const rt = new Uint8Array(512), St = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    rt[e] = t, St[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    rt[e] = rt[e - 255];
})();
kt.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return St[t];
};
kt.exp = function(t) {
  return rt[t];
};
kt.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : rt[St[t] + St[e]];
};
(function(i) {
  const t = kt;
  i.mul = function(n, s) {
    const r = new Uint8Array(n.length + s.length - 1);
    for (let o = 0; o < n.length; o++)
      for (let c = 0; c < s.length; c++)
        r[o + c] ^= t.mul(n[o], s[c]);
    return r;
  }, i.mod = function(n, s) {
    let r = new Uint8Array(n);
    for (; r.length - s.length >= 0; ) {
      const o = r[0];
      for (let a = 0; a < s.length; a++)
        r[a] ^= t.mul(s[a], o);
      let c = 0;
      for (; c < r.length && r[c] === 0; ) c++;
      r = r.slice(c);
    }
    return r;
  }, i.generateECPolynomial = function(n) {
    let s = new Uint8Array([1]);
    for (let r = 0; r < n; r++)
      s = i.mul(s, new Uint8Array([1, t.exp(r)]));
    return s;
  };
})(ke);
const Ne = ke;
function Qt(i) {
  this.genPoly = void 0, this.degree = i, this.degree && this.initialize(this.degree);
}
Qt.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = Ne.generateECPolynomial(this.degree);
};
Qt.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const n = Ne.mod(e, this.genPoly), s = this.degree - n.length;
  if (s > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(n, s), r;
  }
  return n;
};
var fi = Qt, Me = {}, F = {}, Zt = {};
Zt.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var B = {};
const Ie = "[0-9]+", gi = "[A-Z $%*+\\-./:]+";
let ht = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
ht = ht.replace(/u/g, "\\u");
const pi = "(?:(?![A-Z0-9 $%*+\\-./:]|" + ht + `)(?:.|[\r
]))+`;
B.KANJI = new RegExp(ht, "g");
B.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
B.BYTE = new RegExp(pi, "g");
B.NUMERIC = new RegExp(Ie, "g");
B.ALPHANUMERIC = new RegExp(gi, "g");
const _i = new RegExp("^" + ht + "$"), mi = new RegExp("^" + Ie + "$"), wi = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
B.testKanji = function(t) {
  return _i.test(t);
};
B.testNumeric = function(t) {
  return mi.test(t);
};
B.testAlphanumeric = function(t) {
  return wi.test(t);
};
(function(i) {
  const t = Zt, e = B;
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
  function n(s) {
    if (typeof s != "string")
      throw new Error("Param is not a string");
    switch (s.toLowerCase()) {
      case "numeric":
        return i.NUMERIC;
      case "alphanumeric":
        return i.ALPHANUMERIC;
      case "kanji":
        return i.KANJI;
      case "byte":
        return i.BYTE;
      default:
        throw new Error("Unknown mode: " + s);
    }
  }
  i.from = function(r, o) {
    if (i.isValid(r))
      return r;
    try {
      return n(r);
    } catch {
      return o;
    }
  };
})(F);
(function(i) {
  const t = N, e = Pt, n = $t, s = F, r = Zt, o = 7973, c = t.getBCHDigit(o);
  function a(d, u, _) {
    for (let w = 1; w <= 40; w++)
      if (u <= i.getCapacity(w, _, d))
        return w;
  }
  function l(d, u) {
    return s.getCharCountIndicator(d, u) + 4;
  }
  function h(d, u) {
    let _ = 0;
    return d.forEach(function(w) {
      const P = l(w.mode, u);
      _ += P + w.getBitsLength();
    }), _;
  }
  function f(d, u) {
    for (let _ = 1; _ <= 40; _++)
      if (h(d, _) <= i.getCapacity(_, u, s.MIXED))
        return _;
  }
  i.from = function(u, _) {
    return r.isValid(u) ? parseInt(u, 10) : _;
  }, i.getCapacity = function(u, _, w) {
    if (!r.isValid(u))
      throw new Error("Invalid QR Code version");
    typeof w > "u" && (w = s.BYTE);
    const P = t.getSymbolTotalCodewords(u), m = e.getTotalCodewordsCount(u, _), y = (P - m) * 8;
    if (w === s.MIXED) return y;
    const p = y - l(w, u);
    switch (w) {
      case s.NUMERIC:
        return Math.floor(p / 10 * 3);
      case s.ALPHANUMERIC:
        return Math.floor(p / 11 * 2);
      case s.KANJI:
        return Math.floor(p / 13);
      case s.BYTE:
      default:
        return Math.floor(p / 8);
    }
  }, i.getBestVersionForData = function(u, _) {
    let w;
    const P = n.from(_, n.M);
    if (Array.isArray(u)) {
      if (u.length > 1)
        return f(u, P);
      if (u.length === 0)
        return 1;
      w = u[0];
    } else
      w = u;
    return a(w.mode, w.getLength(), P);
  }, i.getEncodedBits = function(u) {
    if (!r.isValid(u) || u < 7)
      throw new Error("Invalid QR Code version");
    let _ = u << 12;
    for (; t.getBCHDigit(_) - c >= 0; )
      _ ^= o << t.getBCHDigit(_) - c;
    return u << 12 | _;
  };
})(Me);
var Te = {};
const Ft = N, Be = 1335, yi = 21522, pe = Ft.getBCHDigit(Be);
Te.getEncodedBits = function(t, e) {
  const n = t.bit << 3 | e;
  let s = n << 10;
  for (; Ft.getBCHDigit(s) - pe >= 0; )
    s ^= Be << Ft.getBCHDigit(s) - pe;
  return (n << 10 | s) ^ yi;
};
var De = {};
const Ei = F;
function Y(i) {
  this.mode = Ei.NUMERIC, this.data = i.toString();
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
  let e, n, s;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    n = this.data.substr(e, 3), s = parseInt(n, 10), t.put(s, 10);
  const r = this.data.length - e;
  r > 0 && (n = this.data.substr(e), s = parseInt(n, 10), t.put(s, r * 3 + 1));
};
var vi = Y;
const Si = F, Rt = [
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
  this.mode = Si.ALPHANUMERIC, this.data = i;
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
    let n = Rt.indexOf(this.data[e]) * 45;
    n += Rt.indexOf(this.data[e + 1]), t.put(n, 11);
  }
  this.data.length % 2 && t.put(Rt.indexOf(this.data[e]), 6);
};
var Ai = Q;
const Ci = F;
function Z(i) {
  this.mode = Ci.BYTE, typeof i == "string" ? this.data = new TextEncoder().encode(i) : this.data = new Uint8Array(i);
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
var bi = Z;
const $i = F, Pi = N;
function X(i) {
  this.mode = $i.KANJI, this.data = i;
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
    let e = Pi.toSJIS(this.data[t]);
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
var ki = X, Re = { exports: {} };
(function(i) {
  var t = {
    single_source_shortest_paths: function(e, n, s) {
      var r = {}, o = {};
      o[n] = 0;
      var c = t.PriorityQueue.make();
      c.push(n, 0);
      for (var a, l, h, f, d, u, _, w, P; !c.empty(); ) {
        a = c.pop(), l = a.value, f = a.cost, d = e[l] || {};
        for (h in d)
          d.hasOwnProperty(h) && (u = d[h], _ = f + u, w = o[h], P = typeof o[h] > "u", (P || w > _) && (o[h] = _, c.push(h, _), r[h] = l));
      }
      if (typeof s < "u" && typeof o[s] > "u") {
        var m = ["Could not find a path from ", n, " to ", s, "."].join("");
        throw new Error(m);
      }
      return r;
    },
    extract_shortest_path_from_predecessor_list: function(e, n) {
      for (var s = [], r = n; r; )
        s.push(r), e[r], r = e[r];
      return s.reverse(), s;
    },
    find_path: function(e, n, s) {
      var r = t.single_source_shortest_paths(e, n, s);
      return t.extract_shortest_path_from_predecessor_list(
        r,
        s
      );
    },
    /**
     * A very naive priority queue implementation.
     */
    PriorityQueue: {
      make: function(e) {
        var n = t.PriorityQueue, s = {}, r;
        e = e || {};
        for (r in n)
          n.hasOwnProperty(r) && (s[r] = n[r]);
        return s.queue = [], s.sorter = e.sorter || n.default_sorter, s;
      },
      default_sorter: function(e, n) {
        return e.cost - n.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(e, n) {
        var s = { value: e, cost: n };
        this.queue.push(s), this.queue.sort(this.sorter);
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
})(Re);
var Ni = Re.exports;
(function(i) {
  const t = F, e = vi, n = Ai, s = bi, r = ki, o = B, c = N, a = Ni;
  function l(m) {
    return unescape(encodeURIComponent(m)).length;
  }
  function h(m, y, p) {
    const g = [];
    let E;
    for (; (E = m.exec(p)) !== null; )
      g.push({
        data: E[0],
        index: E.index,
        mode: y,
        length: E[0].length
      });
    return g;
  }
  function f(m) {
    const y = h(o.NUMERIC, t.NUMERIC, m), p = h(o.ALPHANUMERIC, t.ALPHANUMERIC, m);
    let g, E;
    return c.isKanjiModeEnabled() ? (g = h(o.BYTE, t.BYTE, m), E = h(o.KANJI, t.KANJI, m)) : (g = h(o.BYTE_KANJI, t.BYTE, m), E = []), y.concat(p, g, E).sort(function(b, M) {
      return b.index - M.index;
    }).map(function(b) {
      return {
        data: b.data,
        mode: b.mode,
        length: b.length
      };
    });
  }
  function d(m, y) {
    switch (y) {
      case t.NUMERIC:
        return e.getBitsLength(m);
      case t.ALPHANUMERIC:
        return n.getBitsLength(m);
      case t.KANJI:
        return r.getBitsLength(m);
      case t.BYTE:
        return s.getBitsLength(m);
    }
  }
  function u(m) {
    return m.reduce(function(y, p) {
      const g = y.length - 1 >= 0 ? y[y.length - 1] : null;
      return g && g.mode === p.mode ? (y[y.length - 1].data += p.data, y) : (y.push(p), y);
    }, []);
  }
  function _(m) {
    const y = [];
    for (let p = 0; p < m.length; p++) {
      const g = m[p];
      switch (g.mode) {
        case t.NUMERIC:
          y.push([
            g,
            { data: g.data, mode: t.ALPHANUMERIC, length: g.length },
            { data: g.data, mode: t.BYTE, length: g.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          y.push([
            g,
            { data: g.data, mode: t.BYTE, length: g.length }
          ]);
          break;
        case t.KANJI:
          y.push([
            g,
            { data: g.data, mode: t.BYTE, length: l(g.data) }
          ]);
          break;
        case t.BYTE:
          y.push([
            { data: g.data, mode: t.BYTE, length: l(g.data) }
          ]);
      }
    }
    return y;
  }
  function w(m, y) {
    const p = {}, g = { start: {} };
    let E = ["start"];
    for (let S = 0; S < m.length; S++) {
      const b = m[S], M = [];
      for (let U = 0; U < b.length; U++) {
        const T = b[U], et = "" + S + U;
        M.push(et), p[et] = { node: T, lastCount: 0 }, g[et] = {};
        for (let Mt = 0; Mt < E.length; Mt++) {
          const D = E[Mt];
          p[D] && p[D].node.mode === T.mode ? (g[D][et] = d(p[D].lastCount + T.length, T.mode) - d(p[D].lastCount, T.mode), p[D].lastCount += T.length) : (p[D] && (p[D].lastCount = T.length), g[D][et] = d(T.length, T.mode) + 4 + t.getCharCountIndicator(T.mode, y));
        }
      }
      E = M;
    }
    for (let S = 0; S < E.length; S++)
      g[E[S]].end = 0;
    return { map: g, table: p };
  }
  function P(m, y) {
    let p;
    const g = t.getBestModeForData(m);
    if (p = t.from(y, g), p !== t.BYTE && p.bit < g.bit)
      throw new Error('"' + m + '" cannot be encoded with mode ' + t.toString(p) + `.
 Suggested mode is: ` + t.toString(g));
    switch (p === t.KANJI && !c.isKanjiModeEnabled() && (p = t.BYTE), p) {
      case t.NUMERIC:
        return new e(m);
      case t.ALPHANUMERIC:
        return new n(m);
      case t.KANJI:
        return new r(m);
      case t.BYTE:
        return new s(m);
    }
  }
  i.fromArray = function(y) {
    return y.reduce(function(p, g) {
      return typeof g == "string" ? p.push(P(g, null)) : g.data && p.push(P(g.data, g.mode)), p;
    }, []);
  }, i.fromString = function(y, p) {
    const g = f(y, c.isKanjiModeEnabled()), E = _(g), S = w(E, p), b = a.find_path(S.map, "start", "end"), M = [];
    for (let U = 1; U < b.length - 1; U++)
      M.push(S.table[b[U]].node);
    return i.fromArray(u(M));
  }, i.rawSplit = function(y) {
    return i.fromArray(
      f(y, c.isKanjiModeEnabled())
    );
  };
})(De);
const Nt = N, xt = $t, Mi = hi, Ii = ui, Ti = be, Bi = $e, Vt = Pe, zt = Pt, Di = fi, At = Me, Ri = Te, xi = F, Ut = De;
function Ui(i, t) {
  const e = i.size, n = Bi.getPositions(t);
  for (let s = 0; s < n.length; s++) {
    const r = n[s][0], o = n[s][1];
    for (let c = -1; c <= 7; c++)
      if (!(r + c <= -1 || e <= r + c))
        for (let a = -1; a <= 7; a++)
          o + a <= -1 || e <= o + a || (c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 2 && c <= 4 && a >= 2 && a <= 4 ? i.set(r + c, o + a, !0, !0) : i.set(r + c, o + a, !1, !0));
  }
}
function Li(i) {
  const t = i.size;
  for (let e = 8; e < t - 8; e++) {
    const n = e % 2 === 0;
    i.set(e, 6, n, !0), i.set(6, e, n, !0);
  }
}
function Oi(i, t) {
  const e = Ti.getPositions(t);
  for (let n = 0; n < e.length; n++) {
    const s = e[n][0], r = e[n][1];
    for (let o = -2; o <= 2; o++)
      for (let c = -2; c <= 2; c++)
        o === -2 || o === 2 || c === -2 || c === 2 || o === 0 && c === 0 ? i.set(s + o, r + c, !0, !0) : i.set(s + o, r + c, !1, !0);
  }
}
function Hi(i, t) {
  const e = i.size, n = At.getEncodedBits(t);
  let s, r, o;
  for (let c = 0; c < 18; c++)
    s = Math.floor(c / 3), r = c % 3 + e - 8 - 3, o = (n >> c & 1) === 1, i.set(s, r, o, !0), i.set(r, s, o, !0);
}
function Lt(i, t, e) {
  const n = i.size, s = Ri.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (s >> r & 1) === 1, r < 6 ? i.set(r, 8, o, !0) : r < 8 ? i.set(r + 1, 8, o, !0) : i.set(n - 15 + r, 8, o, !0), r < 8 ? i.set(8, n - r - 1, o, !0) : r < 9 ? i.set(8, 15 - r - 1 + 1, o, !0) : i.set(8, 15 - r - 1, o, !0);
  i.set(n - 8, 8, 1, !0);
}
function Fi(i, t) {
  const e = i.size;
  let n = -1, s = e - 1, r = 7, o = 0;
  for (let c = e - 1; c > 0; c -= 2)
    for (c === 6 && c--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!i.isReserved(s, c - a)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), i.set(s, c - a, l), r--, r === -1 && (o++, r = 7);
        }
      if (s += n, s < 0 || e <= s) {
        s -= n, n = -n;
        break;
      }
    }
}
function Vi(i, t, e) {
  const n = new Mi();
  e.forEach(function(a) {
    n.put(a.mode.bit, 4), n.put(a.getLength(), xi.getCharCountIndicator(a.mode, i)), a.write(n);
  });
  const s = Nt.getSymbolTotalCodewords(i), r = zt.getTotalCodewordsCount(i, t), o = (s - r) * 8;
  for (n.getLengthInBits() + 4 <= o && n.put(0, 4); n.getLengthInBits() % 8 !== 0; )
    n.putBit(0);
  const c = (o - n.getLengthInBits()) / 8;
  for (let a = 0; a < c; a++)
    n.put(a % 2 ? 17 : 236, 8);
  return zi(n, i, t);
}
function zi(i, t, e) {
  const n = Nt.getSymbolTotalCodewords(t), s = zt.getTotalCodewordsCount(t, e), r = n - s, o = zt.getBlocksCount(t, e), c = n % o, a = o - c, l = Math.floor(n / o), h = Math.floor(r / o), f = h + 1, d = l - h, u = new Di(d);
  let _ = 0;
  const w = new Array(o), P = new Array(o);
  let m = 0;
  const y = new Uint8Array(i.buffer);
  for (let b = 0; b < o; b++) {
    const M = b < a ? h : f;
    w[b] = y.slice(_, _ + M), P[b] = u.encode(w[b]), _ += M, m = Math.max(m, M);
  }
  const p = new Uint8Array(n);
  let g = 0, E, S;
  for (E = 0; E < m; E++)
    for (S = 0; S < o; S++)
      E < w[S].length && (p[g++] = w[S][E]);
  for (E = 0; E < d; E++)
    for (S = 0; S < o; S++)
      p[g++] = P[S][E];
  return p;
}
function ji(i, t, e, n) {
  let s;
  if (Array.isArray(i))
    s = Ut.fromArray(i);
  else if (typeof i == "string") {
    let l = t;
    if (!l) {
      const h = Ut.rawSplit(i);
      l = At.getBestVersionForData(h, e);
    }
    s = Ut.fromString(i, l || 40);
  } else
    throw new Error("Invalid data");
  const r = At.getBestVersionForData(s, e);
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
  const o = Vi(t, e, s), c = Nt.getSymbolSize(t), a = new Ii(c);
  return Ui(a, t), Li(a), Oi(a, t), Lt(a, e, 0), t >= 7 && Hi(a, t), Fi(a, o), isNaN(n) && (n = Vt.getBestMask(
    a,
    Lt.bind(null, a, e)
  )), Vt.applyMask(n, a), Lt(a, e, n), {
    modules: a,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: n,
    segments: s
  };
}
Ae.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let n = xt.M, s, r;
  return typeof e < "u" && (n = xt.from(e.errorCorrectionLevel, xt.M), s = At.from(e.version), r = Vt.from(e.maskPattern), e.toSJISFunc && Nt.setToSJISFunction(e.toSJISFunc)), ji(t, s, n, r);
};
var xe = {}, Xt = {};
(function(i) {
  function t(e) {
    if (typeof e == "number" && (e = e.toString()), typeof e != "string")
      throw new Error("Color should be defined as hex string");
    let n = e.slice().replace("#", "").split("");
    if (n.length < 3 || n.length === 5 || n.length > 8)
      throw new Error("Invalid hex color: " + e);
    (n.length === 3 || n.length === 4) && (n = Array.prototype.concat.apply([], n.map(function(r) {
      return [r, r];
    }))), n.length === 6 && n.push("F", "F");
    const s = parseInt(n.join(""), 16);
    return {
      r: s >> 24 & 255,
      g: s >> 16 & 255,
      b: s >> 8 & 255,
      a: s & 255,
      hex: "#" + n.slice(0, 6).join("")
    };
  }
  i.getOptions = function(n) {
    n || (n = {}), n.color || (n.color = {});
    const s = typeof n.margin > "u" || n.margin === null || n.margin < 0 ? 4 : n.margin, r = n.width && n.width >= 21 ? n.width : void 0, o = n.scale || 4;
    return {
      width: r,
      scale: r ? 4 : o,
      margin: s,
      color: {
        dark: t(n.color.dark || "#000000ff"),
        light: t(n.color.light || "#ffffffff")
      },
      type: n.type,
      rendererOpts: n.rendererOpts || {}
    };
  }, i.getScale = function(n, s) {
    return s.width && s.width >= n + s.margin * 2 ? s.width / (n + s.margin * 2) : s.scale;
  }, i.getImageWidth = function(n, s) {
    const r = i.getScale(n, s);
    return Math.floor((n + s.margin * 2) * r);
  }, i.qrToImageData = function(n, s, r) {
    const o = s.modules.size, c = s.modules.data, a = i.getScale(o, r), l = Math.floor((o + r.margin * 2) * a), h = r.margin * a, f = [r.color.light, r.color.dark];
    for (let d = 0; d < l; d++)
      for (let u = 0; u < l; u++) {
        let _ = (d * l + u) * 4, w = r.color.light;
        if (d >= h && u >= h && d < l - h && u < l - h) {
          const P = Math.floor((d - h) / a), m = Math.floor((u - h) / a);
          w = f[c[P * o + m] ? 1 : 0];
        }
        n[_++] = w.r, n[_++] = w.g, n[_++] = w.b, n[_] = w.a;
      }
  };
})(Xt);
(function(i) {
  const t = Xt;
  function e(s, r, o) {
    s.clearRect(0, 0, r.width, r.height), r.style || (r.style = {}), r.height = o, r.width = o, r.style.height = o + "px", r.style.width = o + "px";
  }
  function n() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  i.render = function(r, o, c) {
    let a = c, l = o;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), o || (l = n()), a = t.getOptions(a);
    const h = t.getImageWidth(r.modules.size, a), f = l.getContext("2d"), d = f.createImageData(h, h);
    return t.qrToImageData(d.data, r, a), e(f, l, h), f.putImageData(d, 0, 0), l;
  }, i.renderToDataURL = function(r, o, c) {
    let a = c;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), a || (a = {});
    const l = i.render(r, o, a), h = a.type || "image/png", f = a.rendererOpts || {};
    return l.toDataURL(h, f.quality);
  };
})(xe);
var Ue = {};
const Gi = Xt;
function _e(i, t) {
  const e = i.a / 255, n = t + '="' + i.hex + '"';
  return e < 1 ? n + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : n;
}
function Ot(i, t, e) {
  let n = i + t;
  return typeof e < "u" && (n += " " + e), n;
}
function Ki(i, t, e) {
  let n = "", s = 0, r = !1, o = 0;
  for (let c = 0; c < i.length; c++) {
    const a = Math.floor(c % t), l = Math.floor(c / t);
    !a && !r && (r = !0), i[c] ? (o++, c > 0 && a > 0 && i[c - 1] || (n += r ? Ot("M", a + e, 0.5 + l + e) : Ot("m", s, 0), s = 0, r = !1), a + 1 < t && i[c + 1] || (n += Ot("h", o), o = 0)) : s++;
  }
  return n;
}
Ue.render = function(t, e, n) {
  const s = Gi.getOptions(e), r = t.modules.size, o = t.modules.data, c = r + s.margin * 2, a = s.color.light.a ? "<path " + _e(s.color.light, "fill") + ' d="M0 0h' + c + "v" + c + 'H0z"/>' : "", l = "<path " + _e(s.color.dark, "stroke") + ' d="' + Ki(o, r, s.margin) + '"/>', h = 'viewBox="0 0 ' + c + " " + c + '"', d = '<svg xmlns="http://www.w3.org/2000/svg" ' + (s.width ? 'width="' + s.width + '" height="' + s.width + '" ' : "") + h + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof n == "function" && n(null, d), d;
};
const qi = ci, jt = Ae, Le = xe, Wi = Ue;
function te(i, t, e, n, s) {
  const r = [].slice.call(arguments, 1), o = r.length, c = typeof r[o - 1] == "function";
  if (!c && !qi())
    throw new Error("Callback required as last argument");
  if (c) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (s = e, e = t, t = n = void 0) : o === 3 && (t.getContext && typeof s > "u" ? (s = n, n = void 0) : (s = n, n = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = n = void 0) : o === 2 && !t.getContext && (n = e, e = t, t = void 0), new Promise(function(a, l) {
      try {
        const h = jt.create(e, n);
        a(i(h, t, n));
      } catch (h) {
        l(h);
      }
    });
  }
  try {
    const a = jt.create(e, n);
    s(null, i(a, t, n));
  } catch (a) {
    s(a);
  }
}
gt.create = jt.create;
gt.toCanvas = te.bind(null, Le.render);
gt.toDataURL = te.bind(null, Le.renderToDataURL);
gt.toString = te.bind(null, function(i, t, e) {
  return Wi.render(i, e);
});
var Ji = Object.defineProperty, Yi = Object.getOwnPropertyDescriptor, I = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? Yi(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && Ji(t, e, s), s;
};
let x = class extends R {
  constructor() {
    super(...arguments), this._networks = [], this._ssids = [], this._selectedNetwork = "", this._loading = !1;
  }
  setConfig(i) {
    this._config = i;
  }
  firstUpdated(i) {
    super.firstUpdated(i), this._fetchInitialData();
  }
  async _fetchInitialData() {
    if (this.hass) {
      this._loading = !0;
      try {
        const i = await this.hass.callWS({
          type: "config_entries/get",
          domain: "meraki_ha"
        }), t = i.length > 0 ? i[0].entry_id : null;
        if (!t) return;
        const e = await Ht(this.hass, {
          type: vt.GET_CONFIG,
          config_entry_id: t
        });
        this._networks = (Array.isArray(e.networks) ? e.networks : []).filter((n) => {
          var s;
          return (s = n.productTypes) == null ? void 0 : s.includes("wireless");
        }), this._ssids = Array.isArray(e.ssids) ? e.ssids : [];
      } catch (i) {
        console.error("Failed to fetch Meraki data:", i);
      } finally {
        this._loading = !1;
      }
    }
  }
  _handleNetworkChange(i) {
    i.stopPropagation(), this._selectedNetwork = i.target.value;
  }
  _handleSSIDSelect(i) {
    i.stopPropagation();
    const t = i.target.value, e = this._ssids.find((n) => n.networkId === this._selectedNetwork && String(n.number) === t);
    if (e && this._config) {
      const n = {
        ...this._config,
        ssid: e.name,
        password: e.psk || ""
      };
      this._config = n, this._dispatchEvent(n);
    }
  }
  _valueChanged(i) {
    if (!this._config) return;
    const t = i.target, e = t.configValue;
    if (this._config[e] === t.value) return;
    const n = {
      ...this._config,
      [e]: t.value
    };
    this._config = n, this._dispatchEvent(n);
  }
  _dispatchEvent(i) {
    const t = new CustomEvent("config-changed", {
      detail: { config: i },
      bubbles: !0,
      composed: !0
    });
    this.dispatchEvent(t);
  }
  render() {
    if (!this.hass || !this._config) return A``;
    const i = this._ssids.filter((t) => t.networkId === this._selectedNetwork);
    return A`
      <div class="card-config">
        <ha-select
          label="Network (Optional - to populate SSID)"
          value="${this._selectedNetwork}"
          @closed="${this._handleNetworkChange}"
          fixedMenuPosition
          naturalMenuWidth
        >
          <mwc-list-item value="">Select a network</mwc-list-item>
          ${this._networks.map((t) => A`<mwc-list-item value="${t.id}">${t.name}</mwc-list-item>`)}
        </ha-select>

        <ha-select
          label="SSID from Meraki"
          value=""
          .disabled="${!this._selectedNetwork}"
          @closed="${this._handleSSIDSelect}"
          fixedMenuPosition
          naturalMenuWidth
        >
          <mwc-list-item value="">Select an SSID</mwc-list-item>
          ${i.map((t) => A`<mwc-list-item value="${String(t.number)}">${t.name}</mwc-list-item>`)}
        </ha-select>

        <ha-textfield
          label="SSID Name or Entity ID"
          .value="${this._config.ssid || ""}"
          .configValue="${"ssid"}"
          @input="${this._valueChanged}"
        ></ha-textfield>

        <ha-textfield
          label="Password or Entity ID"
          .value="${this._config.password || ""}"
          .configValue="${"password"}"
          @input="${this._valueChanged}"
        ></ha-textfield>

        <ha-textfield
          label="Card Title"
          .value="${this._config.name || ""}"
          .configValue="${"name"}"
          @input="${this._valueChanged}"
        ></ha-textfield>
      </div>
    `;
  }
};
x.styles = dt`
    .card-config {
      display: flex;
      flex-direction: column;
      gap: 16px;
      padding: 16px;
    }
    ha-select, ha-textfield {
      width: 100%;
    }
  `;
I([
  tt({ attribute: !1 })
], x.prototype, "hass", 2);
I([
  v()
], x.prototype, "_config", 2);
I([
  v()
], x.prototype, "_networks", 2);
I([
  v()
], x.prototype, "_ssids", 2);
I([
  v()
], x.prototype, "_selectedNetwork", 2);
I([
  v()
], x.prototype, "_loading", 2);
x = I([
  bt("meraki-wifi-qr-card-editor")
], x);
let K = class extends R {
  constructor() {
    super(...arguments), this._qrSvg = "";
  }
  static async getConfigElement() {
    return document.createElement("meraki-wifi-qr-card-editor");
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
    var t, e, n, s;
    if (i.has("hass") || i.has("_config")) {
      const r = i.has("hass") ? this._getValueFromHass((t = this._config) == null ? void 0 : t.ssid, i.get("hass")) : null, o = this._getValue((e = this._config) == null ? void 0 : e.ssid), c = i.has("hass") ? this._getValueFromHass((n = this._config) == null ? void 0 : n.password, i.get("hass")) : null, a = this._getValue((s = this._config) == null ? void 0 : s.password);
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
    const e = i.replace(/([\\;,":])/g, "\\$1"), n = t ? t.replace(/([\\;,":])/g, "\\$1") : "";
    return n ? `WIFI:T:WPA;S:${e};P:${n};;` : `WIFI:T:nopass;S:${e};P:;;`;
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
      this._qrSvg = await gt.toString(e, {
        type: "svg",
        margin: 2,
        color: {
          dark: "#000000",
          light: "#ffffff"
        }
      });
    } catch (n) {
      console.error("Failed to generate QR code", n), this._qrSvg = "";
    }
  }
  render() {
    if (!this._config || !this.hass)
      return A``;
    const i = this._getValue(this._config.ssid), t = this._getValue(this._config.password);
    return A`
      <ha-card .header="${this._config.name || "Wi-Fi Access"}">
        <div class="card-content">
          <div class="ssid-display">${i}</div>
          <div class="qr-container" .innerHTML="${this._qrSvg}"></div>
          ${t ? A`<div class="password-display">Password: <code>${t}</code></div>` : ""}
        </div>
      </ha-card>
    `;
  }
};
K.styles = dt`
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
I([
  tt({ attribute: !1 })
], K.prototype, "hass", 2);
I([
  v()
], K.prototype, "_config", 2);
I([
  v()
], K.prototype, "_qrSvg", 2);
K = I([
  bt("meraki-wifi-qr-card")
], K);
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", K);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var Qi = Object.defineProperty, Zi = Object.getOwnPropertyDescriptor, ee = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? Zi(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && Qi(t, e, s), s;
};
let ut = class extends R {
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
      return A`
        <div class="status-item">
          <svg height="12" width="12">
            <circle cx="6" cy="6" r="6" fill="var(--disabled-text-color)" />
          </svg>
          <span class="status-label">${t}</span>
        </div>
      `;
    const e = this.hass.states[i], n = e ? e.state.toLowerCase() : "unknown";
    let s = "var(--disabled-text-color)";
    return n === "ok" || n === "online" || n === "connected" ? s = "var(--success-color)" : n === "warning" ? s = "var(--warning-color)" : (n === "error" || n === "offline" || n === "failed") && (s = "var(--error-color)"), A`
      <div class="status-item">
        <svg height="12" width="12">
          <circle cx="6" cy="6" r="6" fill="${s}" />
        </svg>
        <span class="status-label">${t}</span>
      </div>
    `;
  }
  render() {
    if (!this._config || !this.hass)
      return A``;
    const i = this._config.throughput_entity, t = i && this.hass.states[i] ? this.hass.states[i].state + " " + (this.hass.states[i].attributes.unit_of_measurement || "") : "N/A";
    return A`
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
ut.styles = dt`
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
ee([
  tt({ attribute: !1 })
], ut.prototype, "hass", 2);
ee([
  v()
], ut.prototype, "_config", 2);
ut = ee([
  bt("meraki-network-vitals-card")
], ut);
window.customCards = window.customCards || [];
window.customCards.some((i) => i.type === "meraki-network-vitals-card") || window.customCards.push({
  type: "meraki-network-vitals-card",
  name: "Meraki Network Vitals",
  description: "Compact horizontal header for Meraki network health and throughput.",
  preview: !0
});
var Xi = Object.defineProperty, k = (i, t, e, n) => {
  for (var s = void 0, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = o(t, e, s) || s);
  return s && Xi(t, e, s), s;
};
const ie = class ie extends R {
  constructor() {
    super(...arguments), this._selectedNetwork = "", this._selectedSSID = "", this._selectedPolicy = "", this._selectedDuration = "60", this._customName = "", this._customPassphrase = "", this._creating = !1, this._error = null, this._success = null, this._networks = [], this._ssids = [], this._policies = [], this._loading = !0, this._initDone = !1;
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = t;
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
        }), n = ((t = this._config) == null ? void 0 : t.config_entry_id) || (e.length > 0 ? e[0].entry_id : null);
        if (!n) {
          this._error = "Meraki integration not found. Please configure it first.", this._loading = !1;
          return;
        }
        const s = await Ht(this.hass, {
          type: vt.GET_CONFIG,
          config_entry_id: n
        });
        this._networks = (Array.isArray(s.networks) ? s.networks : []).filter((r) => {
          var o;
          return (o = r.productTypes) == null ? void 0 : o.includes("wireless");
        }), this._ssids = Array.isArray(s.ssids) ? s.ssids : [], this._networks.length > 0 && !this._selectedNetwork && (this._selectedNetwork = this._networks[0].id, this._fetchPolicies(this._selectedNetwork, n));
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
    var n;
    if (this.hass)
      try {
        let s = e || ((n = this._config) == null ? void 0 : n.config_entry_id);
        if (!s) {
          const o = await this.hass.callWS({
            type: "config_entries/get",
            domain: "meraki_ha"
          });
          s = o.length > 0 ? o[0].entry_id : void 0;
        }
        if (!s) return;
        const r = await Ht(this.hass, {
          type: vt.TIMED_ACCESS_GET_POLICIES,
          config_entry_id: s,
          network_id: t
        });
        this._policies = Array.isArray(r) ? r : (r == null ? void 0 : r.policies) || [];
      } catch (s) {
        console.error("Failed to fetch policies:", s), this._policies = [];
      }
  }
  render() {
    var e, n;
    if (this._loading && !this._networks.length)
      return A`
        <ha-card .header="${((e = this._config) == null ? void 0 : e.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    const t = (this._ssids || []).filter((s) => s.networkId === this._selectedNetwork);
    return A`
      <ha-card .header="${((n = this._config) == null ? void 0 : n.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? A`
                <ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => this._error = null}">
                  ${this._error}
                </ha-alert>
              ` : ""}
          ${this._success ? A`
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
      (s) => A`
                  <mwc-list-item value="${s.id}">
                    ${s.name}
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
      (s) => A`
                  <mwc-list-item value="${String(s.number)}">
                    ${s.name} (SSID ${s.number})
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
      (s) => A`
                  <mwc-list-item value="${String(s.groupPolicyId)}">
                    ${s.name}
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
              @input="${(s) => this._customName = s.target.value}"
            ></ha-textfield>

            <ha-textfield
              label="Passphrase (Optional)"
              placeholder="Leave empty to auto-generate"
              .value="${this._customPassphrase}"
              @input="${(s) => this._customPassphrase = s.target.value}"
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
    const n = t.target.value;
    !n || n === this._selectedNetwork || (this._selectedNetwork = n, this._selectedSSID = "", this._selectedPolicy = "", this._fetchSSIDs(), this._fetchPolicies(n));
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
ie.styles = dt`
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
let C = ie;
k([
  tt({ attribute: !1 })
], C.prototype, "hass");
k([
  v()
], C.prototype, "_config");
k([
  v()
], C.prototype, "_selectedNetwork");
k([
  v()
], C.prototype, "_selectedSSID");
k([
  v()
], C.prototype, "_selectedPolicy");
k([
  v()
], C.prototype, "_selectedDuration");
k([
  v()
], C.prototype, "_customName");
k([
  v()
], C.prototype, "_customPassphrase");
k([
  v()
], C.prototype, "_creating");
k([
  v()
], C.prototype, "_error");
k([
  v()
], C.prototype, "_success");
k([
  v()
], C.prototype, "_networks");
k([
  v()
], C.prototype, "_ssids");
k([
  v()
], C.prototype, "_policies");
k([
  v()
], C.prototype, "_loading");
k([
  v()
], C.prototype, "_initDone");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", C);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: !0
});
export {
  C as MerakiGuestAccessCard
};
