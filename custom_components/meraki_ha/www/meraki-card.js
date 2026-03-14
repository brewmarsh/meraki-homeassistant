/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const kt = globalThis, Qt = kt.ShadowRoot && (kt.ShadyCSS === void 0 || kt.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Zt = Symbol(), ge = /* @__PURE__ */ new WeakMap();
let Ne = class {
  constructor(t, e, i) {
    if (this._$cssResult$ = !0, i !== Zt) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Qt && t === void 0) {
      const i = e !== void 0 && e.length === 1;
      i && (t = ge.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), i && ge.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const Qe = (n) => new Ne(typeof n == "string" ? n : n + "", void 0, Zt), F = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((i, s, r) => i + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(s) + n[r + 1], n[0]);
  return new Ne(e, n, Zt);
}, Ze = (n, t) => {
  if (Qt) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const i = document.createElement("style"), s = kt.litNonce;
    s !== void 0 && i.setAttribute("nonce", s), i.textContent = e.cssText, n.appendChild(i);
  }
}, pe = Qt ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const i of t.cssRules) e += i.cssText;
  return Qe(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: Xe, defineProperty: ts, getOwnPropertyDescriptor: es, getOwnPropertyNames: ss, getOwnPropertySymbols: is, getPrototypeOf: ns } = Object, q = globalThis, _e = q.trustedTypes, rs = _e ? _e.emptyScript : "", Ut = q.reactiveElementPolyfillSupport, ut = (n, t) => n, St = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? rs : null;
      break;
    case Object:
    case Array:
      n = n == null ? n : JSON.stringify(n);
  }
  return n;
}, fromAttribute(n, t) {
  let e = n;
  switch (t) {
    case Boolean:
      e = n !== null;
      break;
    case Number:
      e = n === null ? null : Number(n);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(n);
      } catch {
        e = null;
      }
  }
  return e;
} }, Xt = (n, t) => !Xe(n, t), me = { attribute: !0, type: String, converter: St, reflect: !1, useDefault: !1, hasChanged: Xt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), q.litPropertyMetadata ?? (q.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let et = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = me) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const i = Symbol(), s = this.getPropertyDescriptor(t, i, e);
      s !== void 0 && ts(this.prototype, t, s);
    }
  }
  static getPropertyDescriptor(t, e, i) {
    const { get: s, set: r } = es(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: s, set(o) {
      const c = s == null ? void 0 : s.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, c, i);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? me;
  }
  static _$Ei() {
    if (this.hasOwnProperty(ut("elementProperties"))) return;
    const t = ns(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(ut("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(ut("properties"))) {
      const e = this.properties, i = [...ss(e), ...is(e)];
      for (const s of i) this.createProperty(s, e[s]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [i, s] of e) this.elementProperties.set(i, s);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, i] of this.elementProperties) {
      const s = this._$Eu(e, i);
      s !== void 0 && this._$Eh.set(s, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const i = new Set(t.flat(1 / 0).reverse());
      for (const s of i) e.unshift(pe(s));
    } else t !== void 0 && e.push(pe(t));
    return e;
  }
  static _$Eu(t, e) {
    const i = e.attribute;
    return i === !1 ? void 0 : typeof i == "string" ? i : typeof t == "string" ? t.toLowerCase() : void 0;
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
    for (const i of e.keys()) this.hasOwnProperty(i) && (t.set(i, this[i]), delete this[i]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return Ze(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    var t;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$EO) == null || t.forEach((e) => {
      var i;
      return (i = e.hostConnected) == null ? void 0 : i.call(e);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$EO) == null || t.forEach((e) => {
      var i;
      return (i = e.hostDisconnected) == null ? void 0 : i.call(e);
    });
  }
  attributeChangedCallback(t, e, i) {
    this._$AK(t, i);
  }
  _$ET(t, e) {
    var r;
    const i = this.constructor.elementProperties.get(t), s = this.constructor._$Eu(t, i);
    if (s !== void 0 && i.reflect === !0) {
      const o = (((r = i.converter) == null ? void 0 : r.toAttribute) !== void 0 ? i.converter : St).toAttribute(e, i.type);
      this._$Em = t, o == null ? this.removeAttribute(s) : this.setAttribute(s, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const i = this.constructor, s = i._$Eh.get(t);
    if (s !== void 0 && this._$Em !== s) {
      const c = i.getPropertyOptions(s), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((r = c.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? c.converter : St;
      this._$Em = s;
      const l = a.fromAttribute(e, c.type);
      this[s] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(s)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, i, s = !1, r) {
    var o;
    if (t !== void 0) {
      const c = this.constructor;
      if (s === !1 && (r = this[t]), i ?? (i = c.getPropertyOptions(t)), !((i.hasChanged ?? Xt)(r, e) || i.useDefault && i.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(c._$Eu(t, i)))) return;
      this.C(t, e, i);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: i, reflect: s, wrapped: r }, o) {
    i && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || i || (e = void 0), this._$AL.set(t, e)), s === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
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
    var i;
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
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (i = this._$EO) == null || i.forEach((s) => {
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
    (e = this._$EO) == null || e.forEach((i) => {
      var s;
      return (s = i.hostUpdated) == null ? void 0 : s.call(i);
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
et.elementStyles = [], et.shadowRootOptions = { mode: "open" }, et[ut("elementProperties")] = /* @__PURE__ */ new Map(), et[ut("finalized")] = /* @__PURE__ */ new Map(), Ut == null || Ut({ ReactiveElement: et }), (q.reactiveElementVersions ?? (q.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ft = globalThis, ye = (n) => n, Pt = ft.trustedTypes, we = Pt ? Pt.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, De = "$lit$", G = `lit$${Math.random().toFixed(9).slice(2)}$`, Me = "?" + G, os = `<${Me}>`, X = document, pt = () => X.createComment(""), _t = (n) => n === null || typeof n != "object" && typeof n != "function", te = Array.isArray, as = (n) => te(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", Ot = `[
\f\r]`, ht = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, ve = /-->/g, be = />/g, Y = RegExp(`>|${Ot}(?:([^\\s"'>=/]+)(${Ot}*=${Ot}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), Ee = /'/g, $e = /"/g, Te = /^(?:script|style|textarea|title)$/i, cs = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), w = cs(1), it = Symbol.for("lit-noChange"), C = Symbol.for("lit-nothing"), Ae = /* @__PURE__ */ new WeakMap(), Q = X.createTreeWalker(X, 129);
function Ie(n, t) {
  if (!te(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return we !== void 0 ? we.createHTML(t) : t;
}
const ls = (n, t) => {
  const e = n.length - 1, i = [];
  let s, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = ht;
  for (let c = 0; c < e; c++) {
    const a = n[c];
    let l, d, u = -1, f = 0;
    for (; f < a.length && (o.lastIndex = f, d = o.exec(a), d !== null); ) f = o.lastIndex, o === ht ? d[1] === "!--" ? o = ve : d[1] !== void 0 ? o = be : d[2] !== void 0 ? (Te.test(d[2]) && (s = RegExp("</" + d[2], "g")), o = Y) : d[3] !== void 0 && (o = Y) : o === Y ? d[0] === ">" ? (o = s ?? ht, u = -1) : d[1] === void 0 ? u = -2 : (u = o.lastIndex - d[2].length, l = d[1], o = d[3] === void 0 ? Y : d[3] === '"' ? $e : Ee) : o === $e || o === Ee ? o = Y : o === ve || o === be ? o = ht : (o = Y, s = void 0);
    const h = o === Y && n[c + 1].startsWith("/>") ? " " : "";
    r += o === ht ? a + os : u >= 0 ? (i.push(l), a.slice(0, u) + De + a.slice(u) + G + h) : a + G + (u === -2 ? c : h);
  }
  return [Ie(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), i];
};
class mt {
  constructor({ strings: t, _$litType$: e }, i) {
    let s;
    this.parts = [];
    let r = 0, o = 0;
    const c = t.length - 1, a = this.parts, [l, d] = ls(t, e);
    if (this.el = mt.createElement(l, i), Q.currentNode = this.el.content, e === 2 || e === 3) {
      const u = this.el.content.firstChild;
      u.replaceWith(...u.childNodes);
    }
    for (; (s = Q.nextNode()) !== null && a.length < c; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) for (const u of s.getAttributeNames()) if (u.endsWith(De)) {
          const f = d[o++], h = s.getAttribute(u).split(G), g = /([.?@])?(.*)/.exec(f);
          a.push({ type: 1, index: r, name: g[2], strings: h, ctor: g[1] === "." ? hs : g[1] === "?" ? us : g[1] === "@" ? fs : Mt }), s.removeAttribute(u);
        } else u.startsWith(G) && (a.push({ type: 6, index: r }), s.removeAttribute(u));
        if (Te.test(s.tagName)) {
          const u = s.textContent.split(G), f = u.length - 1;
          if (f > 0) {
            s.textContent = Pt ? Pt.emptyScript : "";
            for (let h = 0; h < f; h++) s.append(u[h], pt()), Q.nextNode(), a.push({ type: 2, index: ++r });
            s.append(u[f], pt());
          }
        }
      } else if (s.nodeType === 8) if (s.data === Me) a.push({ type: 2, index: r });
      else {
        let u = -1;
        for (; (u = s.data.indexOf(G, u + 1)) !== -1; ) a.push({ type: 7, index: r }), u += G.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const i = X.createElement("template");
    return i.innerHTML = t, i;
  }
}
function nt(n, t, e = n, i) {
  var o, c;
  if (t === it) return t;
  let s = i !== void 0 ? (o = e._$Co) == null ? void 0 : o[i] : e._$Cl;
  const r = _t(t) ? void 0 : t._$litDirective$;
  return (s == null ? void 0 : s.constructor) !== r && ((c = s == null ? void 0 : s._$AO) == null || c.call(s, !1), r === void 0 ? s = void 0 : (s = new r(n), s._$AT(n, e, i)), i !== void 0 ? (e._$Co ?? (e._$Co = []))[i] = s : e._$Cl = s), s !== void 0 && (t = nt(n, s._$AS(n, t.values), s, i)), t;
}
class ds {
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
    const { el: { content: e }, parts: i } = this._$AD, s = ((t == null ? void 0 : t.creationScope) ?? X).importNode(e, !0);
    Q.currentNode = s;
    let r = Q.nextNode(), o = 0, c = 0, a = i[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let l;
        a.type === 2 ? l = new bt(r, r.nextSibling, this, t) : a.type === 1 ? l = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (l = new gs(r, this, t)), this._$AV.push(l), a = i[++c];
      }
      o !== (a == null ? void 0 : a.index) && (r = Q.nextNode(), o++);
    }
    return Q.currentNode = X, s;
  }
  p(t) {
    let e = 0;
    for (const i of this._$AV) i !== void 0 && (i.strings !== void 0 ? (i._$AI(t, i, e), e += i.strings.length - 2) : i._$AI(t[e])), e++;
  }
}
class bt {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, i, s) {
    this.type = 2, this._$AH = C, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = i, this.options = s, this._$Cv = (s == null ? void 0 : s.isConnected) ?? !0;
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
    t = nt(this, t, e), _t(t) ? t === C || t == null || t === "" ? (this._$AH !== C && this._$AR(), this._$AH = C) : t !== this._$AH && t !== it && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : as(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== C && _t(this._$AH) ? this._$AA.nextSibling.data = t : this.T(X.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: i } = t, s = typeof i == "number" ? this._$AC(t) : (i.el === void 0 && (i.el = mt.createElement(Ie(i.h, i.h[0]), this.options)), i);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === s) this._$AH.p(e);
    else {
      const o = new ds(s, this), c = o.u(this.options);
      o.p(e), this.T(c), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = Ae.get(t.strings);
    return e === void 0 && Ae.set(t.strings, e = new mt(t)), e;
  }
  k(t) {
    te(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let i, s = 0;
    for (const r of t) s === e.length ? e.push(i = new bt(this.O(pt()), this.O(pt()), this, this.options)) : i = e[s], i._$AI(r), s++;
    s < e.length && (this._$AR(i && i._$AB.nextSibling, s), e.length = s);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var i;
    for ((i = this._$AP) == null ? void 0 : i.call(this, !1, !0, e); t !== this._$AB; ) {
      const s = ye(t).nextSibling;
      ye(t).remove(), t = s;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class Mt {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, i, s, r) {
    this.type = 1, this._$AH = C, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = r, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = C;
  }
  _$AI(t, e = this, i, s) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = nt(this, t, e, 0), o = !_t(t) || t !== this._$AH && t !== it, o && (this._$AH = t);
    else {
      const c = t;
      let a, l;
      for (t = r[0], a = 0; a < r.length - 1; a++) l = nt(this, c[i + a], e, a), l === it && (l = this._$AH[a]), o || (o = !_t(l) || l !== this._$AH[a]), l === C ? t = C : t !== C && (t += (l ?? "") + r[a + 1]), this._$AH[a] = l;
    }
    o && !s && this.j(t);
  }
  j(t) {
    t === C ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class hs extends Mt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === C ? void 0 : t;
  }
}
class us extends Mt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== C);
  }
}
class fs extends Mt {
  constructor(t, e, i, s, r) {
    super(t, e, i, s, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = nt(this, t, e, 0) ?? C) === it) return;
    const i = this._$AH, s = t === C && i !== C || t.capture !== i.capture || t.once !== i.once || t.passive !== i.passive, r = t !== C && (i === C || s);
    s && this.element.removeEventListener(this.name, this, i), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class gs {
  constructor(t, e, i) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    nt(this, t);
  }
}
const zt = ft.litHtmlPolyfillSupport;
zt == null || zt(mt, bt), (ft.litHtmlVersions ?? (ft.litHtmlVersions = [])).push("3.3.2");
const ps = (n, t, e) => {
  const i = (e == null ? void 0 : e.renderBefore) ?? t;
  let s = i._$litPart$;
  if (s === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    i._$litPart$ = s = new bt(t.insertBefore(pt(), r), r, void 0, e ?? {});
  }
  return s._$AI(n), s;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Z = globalThis;
class D extends et {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = ps(e, this.renderRoot, this.renderOptions);
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
    return it;
  }
}
var Pe;
D._$litElement$ = !0, D.finalized = !0, (Pe = Z.litElementHydrateSupport) == null || Pe.call(Z, { LitElement: D });
const Ht = Z.litElementPolyfillSupport;
Ht == null || Ht({ LitElement: D });
(Z.litElementVersions ?? (Z.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const _s = { attribute: !0, type: String, converter: St, reflect: !1, hasChanged: Xt }, ms = (n = _s, t, e) => {
  const { kind: i, metadata: s } = e;
  let r = globalThis.litPropertyMetadata.get(s);
  if (r === void 0 && globalThis.litPropertyMetadata.set(s, r = /* @__PURE__ */ new Map()), i === "setter" && ((n = Object.create(n)).wrapped = !0), r.set(e.name, n), i === "accessor") {
    const { name: o } = e;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(o, a, n, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(o, void 0, n, c), c;
    } };
  }
  if (i === "setter") {
    const { name: o } = e;
    return function(c) {
      const a = this[o];
      t.call(this, c), this.requestUpdate(o, a, n, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + i);
};
function j(n) {
  return (t, e) => typeof e == "object" ? ms(n, t, e) : ((i, s, r) => {
    const o = s.hasOwnProperty(r);
    return s.constructor.createProperty(r, i), o ? Object.getOwnPropertyDescriptor(s, r) : void 0;
  })(n, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function y(n) {
  return j({ ...n, state: !0, attribute: !1 });
}
const ee = (n, t) => w`
  <div class="meraki-warning">
    <ha-icon icon="mdi:information"></ha-icon>
    <div class="warning-content">
      <strong>${n}</strong>
      <p>${t}</p>
    </div>
  </div>
`, ys = (n) => w`
  <div class="meraki-loading">
    <ha-circular-progress active></ha-circular-progress>
    <span>${n}</span>
  </div>
`, Tt = F`
  .meraki-warning {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    background-color: var(--warning-color);
    color: var(--primary-text-color);
    border-radius: 8px;
  }
  .warning-content strong {
    display: block;
    margin-bottom: 4px;
  }
  .warning-content p {
    margin: 0;
    font-size: 0.9em;
    opacity: 0.9;
  }
  .meraki-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    gap: 12px;
  }
  .version {
    font-size: 9px;
    color: var(--secondary-text-color);
    text-align: right;
    padding: 4px 12px;
    opacity: 0.4;
  }
`;
var xe = /* @__PURE__ */ ((n) => (n.GET_CONFIG = "meraki_ha/get_config", n.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", n.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", n.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", n.GET_VERSION = "meraki_ha/get_version", n.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", n.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", n.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", n.GET_GUEST_KEYS = "meraki_ha/ipsk/get", n.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", n.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", n))(xe || {});
const ws = async (n, t) => {
  if (!n)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof n.callWS == "function")
      return await n.callWS(t);
    if (n.connection && typeof n.connection.sendMessagePromise == "function")
      return await n.connection.sendMessagePromise(t);
    throw new Error("Home Assistant WebSocket communication methods not found.");
  } catch (e) {
    throw console.error(`Meraki HA: WebSocket error [${t.type}]:`, e), e;
  }
};
class P {
  /**
   * Fetches wireless networks, SSIDs, and group policies directly from the integration's backend cache.
   */
  static async fetchConfig(t) {
    try {
      const e = await t.callWS({
        type: "config_entries/get",
        domain: "meraki_ha"
      }), i = e.length > 0 ? e[0].entry_id : null;
      if (!i)
        return { networks: [], ssids: [], groupPolicies: [], entryId: null };
      const s = await ws(t, {
        type: xe.GET_CONFIG,
        config_entry_id: i
      }), r = (Array.isArray(s.networks) ? s.networks : []).filter((a) => {
        var l;
        return (l = a.productTypes) == null ? void 0 : l.includes("wireless");
      }), o = Array.isArray(s.ssids) ? s.ssids : [], c = [];
      if (s.group_policies && typeof s.group_policies == "object")
        for (const [a, l] of Object.entries(
          s.group_policies
        ))
          Array.isArray(l) && l.forEach((d) => {
            c.push({
              networkId: a,
              groupPolicyId: String(d.groupPolicyId),
              name: d.name
            });
          });
      return { networks: r, ssids: o, groupPolicies: c, entryId: i };
    } catch (e) {
      return console.error("Failed to fetch Meraki data via WS:", e), { networks: [], ssids: [], groupPolicies: [], entryId: null };
    }
  }
  /**
   * Intelligently polls the backend until the API backoffs clear and data is populated.
   * @param hass The Home Assistant instance
   * @param onStatusUpdate Callback fired whenever the loading state or message changes
   * @param maxRetries Maximum number of polling attempts (default: 12 attempts / ~1 minute)
   * @param delayMs Delay between attempts in milliseconds (default: 5000ms)
   */
  static async pollConfig(t, e, i = 12, s = 5e3) {
    for (let r = 0; r < i; r++) {
      try {
        const o = await this.fetchConfig(t);
        if (o.networks.length > 0)
          return e("", !1), o;
        e(
          `Waiting for integration to sync... (Attempt ${r + 1}/${i})`,
          !0
        );
      } catch {
        e(
          `Error connecting to backend. Retrying... (Attempt ${r + 1}/${i})`,
          !0
        );
      }
      await new Promise((o) => setTimeout(o, s));
    }
    return e(
      "Integration failed to initialize after 1 minute. Please check backend logs.",
      !1
    ), { networks: [], ssids: [], groupPolicies: [], entryId: null };
  }
  /**
   * Formats networks for an ha-form dropdown.
   */
  static getNetworkOptions(t, e = !1) {
    const i = t.map((s) => ({ value: s.id, label: s.name }));
    return e ? [{ value: "", label: "All Networks" }, ...i] : i;
  }
  /**
   * Formats SSIDs for an ha-form dropdown.
   * @param valueType Determines if the dropdown returns the SSID's string name (for QR codes) or integer number (for Guest API calls).
   */
  static getSsidOptions(t, e, i = "name") {
    return (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: i === "number" ? String(r.number) : r.name,
      label: `${r.name} (SSID ${r.number})`
    }));
  }
  /**
   * Formats Group Policies for an ha-form dropdown.
   */
  static getGroupPolicyOptions(t, e) {
    const s = (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: r.groupPolicyId,
      label: r.name
    }));
    return [
      { value: "CREATE", label: "Create 'Home Assistant Guest' Policy" },
      { value: "NONE", label: "None (Network Default)" },
      ...s
    ];
  }
}
var vs = Object.defineProperty, J = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && vs(t, e, s), s;
};
const ae = class ae extends D {
  constructor() {
    super(...arguments), this._optimisticProfile = null, this._isUpdating = !1, this._isLoading = !0, this._loadingMessage = "Connecting...";
  }
  static async getConfigElement() {
    return document.createElement("meraki-content-filter-card-editor");
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = { ...t };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    this.hass && await P.pollConfig(
      this.hass,
      (t, e) => {
        this._loadingMessage = t, this._isLoading = e;
      }
    );
  }
  _discoverEntity() {
    if (this.hass)
      return Object.keys(this.hass.states).find((t) => {
        var s;
        if (!t.startsWith("select.")) return !1;
        const i = ((s = this.hass.states[t].attributes.friendly_name) == null ? void 0 : s.toLowerCase()) || "";
        return t.includes("content_filter") || i.includes("content filter") || t.includes("meraki");
      });
  }
  static getStubConfig() {
    return {
      entity: "",
      name: ""
    };
  }
  render() {
    var l, d, u;
    if (!this.hass || !this._config) return w``;
    if (this._isLoading)
      return w`
        <ha-card .header="${((l = this._config) == null ? void 0 : l.name) || "Meraki Content Filter"}">
          <div class="card-content" style="text-align: center; padding: 32px;">
            <ha-circular-progress active></ha-circular-progress>
            <div style="margin-top: 16px; color: var(--secondary-text-color);">
              ${this._loadingMessage}
            </div>
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    const t = this._config.entity || this._discoverEntity(), e = t ? this.hass.states[t] : void 0, i = this._config.entity ? this.hass.states[this._config.entity] : void 0, s = ((d = i == null ? void 0 : i.attributes) == null ? void 0 : d.friendly_name) || "Meraki", r = this._config.name || (this._config.entity ? `${s} Content Filter` : "Meraki Content Filter");
    if (!t || !e)
      return w`
        <ha-card .header="${r}">
          <div class="card-content">
             ${ee("Entity Missing", "No content filter entity was found. Please check your configuration.")}
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    const o = e.state || "Unknown", c = ((u = e.attributes) == null ? void 0 : u.options) || ["None", "Security", "Family", "Strict"], a = this._optimisticProfile || o;
    return w`
      <ha-card .header="${r}">
        <div class="card-content">
          <div class="button-grid">
            ${c.map((f) => {
      const h = a.toLowerCase() === f.toLowerCase(), g = this._isUpdating && this._optimisticProfile === f;
      return w`
                <button
                  class="filter-btn ${h ? "active" : ""} ${this._isUpdating && !g ? "disabled" : ""}"
                  ?disabled=${this._isUpdating}
                  @click=${() => this._setFilterProfile(f, t)}
                >
                  ${g ? w`<ha-circular-progress active size="small"></ha-circular-progress> Saving...` : f}
                </button>
              `;
    })}
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3501"}</div>
      </ha-card>
    `;
  }
  async _setFilterProfile(t, e) {
    if (!(!this.hass || !e || !t || this._isUpdating)) {
      this._isUpdating = !0, this._optimisticProfile = t;
      try {
        await this.hass.callService("select", "select_option", {
          entity_id: e,
          option: t
        }), setTimeout(() => {
          this._optimisticProfile = null, this._isUpdating = !1;
        }, 8e3);
      } catch (i) {
        console.error("Failed to call select_option service:", i), this._optimisticProfile = null, this._isUpdating = !1;
      }
    }
  }
};
ae.styles = [
  Tt,
  F`
      :host { display: block; }
      ha-card {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .card-content { padding: 16px; }
      .button-grid {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .filter-btn {
        width: 100%;
        padding: 12px;
        background: transparent;
        color: var(--primary-text-color, #ffffff);
        border: 1px solid var(--divider-color, #444444);
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
        font-family: inherit;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
      }
      .filter-btn:hover:not(:disabled) {
        background: var(--secondary-background-color, rgba(255,255,255,0.05));
      }
      .filter-btn.active {
        background: var(--success-color, #4caf50);
        color: #ffffff;
        border-color: var(--success-color, #4caf50);
        font-weight: bold;
      }
      .filter-btn.disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }

      /* Style the circular progress to match the text color */
      ha-circular-progress {
        --mdc-theme-primary: currentColor;
      }
    `
];
let O = ae;
J([
  j({ attribute: !1 })
], O.prototype, "hass");
J([
  y()
], O.prototype, "_config");
J([
  y()
], O.prototype, "_optimisticProfile");
J([
  y()
], O.prototype, "_isUpdating");
J([
  y()
], O.prototype, "_isLoading");
J([
  y()
], O.prototype, "_loadingMessage");
const ce = class ce extends D {
  constructor() {
    super(...arguments), this._schema = [
      {
        name: "entity",
        selector: { entity: { domain: "select" } }
      },
      {
        name: "name",
        selector: { text: {} }
      }
    ], this._computeLabel = (t) => t.name === "entity" ? "Entity (Optional)" : t.name === "name" ? "Display Name (Optional)" : t.name;
  }
  setConfig(t) {
    this._config = t;
  }
  render() {
    return !this.hass || !this._config ? w`` : w`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${this._schema}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = { ...this._config, ...t.detail.value };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: e },
      bubbles: !0,
      composed: !0
    }));
  }
};
ce.styles = F`
    .editor-container { padding: 16px; }
  `;
let yt = ce;
J([
  j({ attribute: !1 })
], yt.prototype, "hass");
J([
  y()
], yt.prototype, "_config");
customElements.get("meraki-content-filter-card") || customElements.define("meraki-content-filter-card", O);
customElements.get("meraki-content-filter-card-editor") || customElements.define("meraki-content-filter-card-editor", yt);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-content-filter-card") || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var Et = {}, bs = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, Le = {}, N = {};
let se;
const Es = [
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
  return Es[t];
};
N.getBCHDigit = function(n) {
  let t = 0;
  for (; n !== 0; )
    t++, n >>>= 1;
  return t;
};
N.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  se = t;
};
N.isKanjiModeEnabled = function() {
  return typeof se < "u";
};
N.toSJIS = function(t) {
  return se(t);
};
var It = {};
(function(n) {
  n.L = { bit: 1 }, n.M = { bit: 0 }, n.Q = { bit: 3 }, n.H = { bit: 2 };
  function t(e) {
    if (typeof e != "string")
      throw new Error("Param is not a string");
    switch (e.toLowerCase()) {
      case "l":
      case "low":
        return n.L;
      case "m":
      case "medium":
        return n.M;
      case "q":
      case "quartile":
        return n.Q;
      case "h":
      case "high":
        return n.H;
      default:
        throw new Error("Unknown EC Level: " + e);
    }
  }
  n.isValid = function(i) {
    return i && typeof i.bit < "u" && i.bit >= 0 && i.bit < 4;
  }, n.from = function(i, s) {
    if (n.isValid(i))
      return i;
    try {
      return t(i);
    } catch {
      return s;
    }
  };
})(It);
function Be() {
  this.buffer = [], this.length = 0;
}
Be.prototype = {
  get: function(n) {
    const t = Math.floor(n / 8);
    return (this.buffer[t] >>> 7 - n % 8 & 1) === 1;
  },
  put: function(n, t) {
    for (let e = 0; e < t; e++)
      this.putBit((n >>> t - e - 1 & 1) === 1);
  },
  getLengthInBits: function() {
    return this.length;
  },
  putBit: function(n) {
    const t = Math.floor(this.length / 8);
    this.buffer.length <= t && this.buffer.push(0), n && (this.buffer[t] |= 128 >>> this.length % 8), this.length++;
  }
};
var $s = Be;
function $t(n) {
  if (!n || n < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = n, this.data = new Uint8Array(n * n), this.reservedBit = new Uint8Array(n * n);
}
$t.prototype.set = function(n, t, e, i) {
  const s = n * this.size + t;
  this.data[s] = e, i && (this.reservedBit[s] = !0);
};
$t.prototype.get = function(n, t) {
  return this.data[n * this.size + t];
};
$t.prototype.xor = function(n, t, e) {
  this.data[n * this.size + t] ^= e;
};
$t.prototype.isReserved = function(n, t) {
  return this.reservedBit[n * this.size + t];
};
var As = $t, Re = {};
(function(n) {
  const t = N.getSymbolSize;
  n.getRowColCoords = function(i) {
    if (i === 1) return [];
    const s = Math.floor(i / 7) + 2, r = t(i), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * s - 2)) * 2, c = [r - 7];
    for (let a = 1; a < s - 1; a++)
      c[a] = c[a - 1] - o;
    return c.push(6), c.reverse();
  }, n.getPositions = function(i) {
    const s = [], r = n.getRowColCoords(i), o = r.length;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        c === 0 && a === 0 || // top-left
        c === 0 && a === o - 1 || // bottom-left
        c === o - 1 && a === 0 || s.push([r[c], r[a]]);
    return s;
  };
})(Re);
var Ue = {};
const Cs = N.getSymbolSize, Ce = 7;
Ue.getPositions = function(t) {
  const e = Cs(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - Ce, 0],
    // bottom-left
    [0, e - Ce]
  ];
};
var Oe = {};
(function(n) {
  n.Patterns = {
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
  n.isValid = function(s) {
    return s != null && s !== "" && !isNaN(s) && s >= 0 && s <= 7;
  }, n.from = function(s) {
    return n.isValid(s) ? parseInt(s, 10) : void 0;
  }, n.getPenaltyN1 = function(s) {
    const r = s.size;
    let o = 0, c = 0, a = 0, l = null, d = null;
    for (let u = 0; u < r; u++) {
      c = a = 0, l = d = null;
      for (let f = 0; f < r; f++) {
        let h = s.get(u, f);
        h === l ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), l = h, c = 1), h = s.get(f, u), h === d ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), d = h, a = 1);
      }
      c >= 5 && (o += t.N1 + (c - 5)), a >= 5 && (o += t.N1 + (a - 5));
    }
    return o;
  }, n.getPenaltyN2 = function(s) {
    const r = s.size;
    let o = 0;
    for (let c = 0; c < r - 1; c++)
      for (let a = 0; a < r - 1; a++) {
        const l = s.get(c, a) + s.get(c, a + 1) + s.get(c + 1, a) + s.get(c + 1, a + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, n.getPenaltyN3 = function(s) {
    const r = s.size;
    let o = 0, c = 0, a = 0;
    for (let l = 0; l < r; l++) {
      c = a = 0;
      for (let d = 0; d < r; d++)
        c = c << 1 & 2047 | s.get(l, d), d >= 10 && (c === 1488 || c === 93) && o++, a = a << 1 & 2047 | s.get(d, l), d >= 10 && (a === 1488 || a === 93) && o++;
    }
    return o * t.N3;
  }, n.getPenaltyN4 = function(s) {
    let r = 0;
    const o = s.data.length;
    for (let a = 0; a < o; a++) r += s.data[a];
    return Math.abs(Math.ceil(r * 100 / o / 5) - 10) * t.N4;
  };
  function e(i, s, r) {
    switch (i) {
      case n.Patterns.PATTERN000:
        return (s + r) % 2 === 0;
      case n.Patterns.PATTERN001:
        return s % 2 === 0;
      case n.Patterns.PATTERN010:
        return r % 3 === 0;
      case n.Patterns.PATTERN011:
        return (s + r) % 3 === 0;
      case n.Patterns.PATTERN100:
        return (Math.floor(s / 2) + Math.floor(r / 3)) % 2 === 0;
      case n.Patterns.PATTERN101:
        return s * r % 2 + s * r % 3 === 0;
      case n.Patterns.PATTERN110:
        return (s * r % 2 + s * r % 3) % 2 === 0;
      case n.Patterns.PATTERN111:
        return (s * r % 3 + (s + r) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + i);
    }
  }
  n.applyMask = function(s, r) {
    const o = r.size;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        r.isReserved(a, c) || r.xor(a, c, e(s, a, c));
  }, n.getBestMask = function(s, r) {
    const o = Object.keys(n.Patterns).length;
    let c = 0, a = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), n.applyMask(l, s);
      const d = n.getPenaltyN1(s) + n.getPenaltyN2(s) + n.getPenaltyN3(s) + n.getPenaltyN4(s);
      n.applyMask(l, s), d < a && (a = d, c = l);
    }
    return c;
  };
})(Oe);
var xt = {};
const K = It, At = [
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
], Ct = [
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
xt.getBlocksCount = function(t, e) {
  switch (e) {
    case K.L:
      return At[(t - 1) * 4 + 0];
    case K.M:
      return At[(t - 1) * 4 + 1];
    case K.Q:
      return At[(t - 1) * 4 + 2];
    case K.H:
      return At[(t - 1) * 4 + 3];
    default:
      return;
  }
};
xt.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case K.L:
      return Ct[(t - 1) * 4 + 0];
    case K.M:
      return Ct[(t - 1) * 4 + 1];
    case K.Q:
      return Ct[(t - 1) * 4 + 2];
    case K.H:
      return Ct[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var ze = {}, Lt = {};
const gt = new Uint8Array(512), Nt = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    gt[e] = t, Nt[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    gt[e] = gt[e - 255];
})();
Lt.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return Nt[t];
};
Lt.exp = function(t) {
  return gt[t];
};
Lt.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : gt[Nt[t] + Nt[e]];
};
(function(n) {
  const t = Lt;
  n.mul = function(i, s) {
    const r = new Uint8Array(i.length + s.length - 1);
    for (let o = 0; o < i.length; o++)
      for (let c = 0; c < s.length; c++)
        r[o + c] ^= t.mul(i[o], s[c]);
    return r;
  }, n.mod = function(i, s) {
    let r = new Uint8Array(i);
    for (; r.length - s.length >= 0; ) {
      const o = r[0];
      for (let a = 0; a < s.length; a++)
        r[a] ^= t.mul(s[a], o);
      let c = 0;
      for (; c < r.length && r[c] === 0; ) c++;
      r = r.slice(c);
    }
    return r;
  }, n.generateECPolynomial = function(i) {
    let s = new Uint8Array([1]);
    for (let r = 0; r < i; r++)
      s = n.mul(s, new Uint8Array([1, t.exp(r)]));
    return s;
  };
})(ze);
const He = ze;
function ie(n) {
  this.genPoly = void 0, this.degree = n, this.degree && this.initialize(this.degree);
}
ie.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = He.generateECPolynomial(this.degree);
};
ie.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const i = He.mod(e, this.genPoly), s = this.degree - i.length;
  if (s > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(i, s), r;
  }
  return i;
};
var ks = ie, Fe = {}, W = {}, ne = {};
ne.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var R = {};
const je = "[0-9]+", Ss = "[A-Z $%*+\\-./:]+";
let wt = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
wt = wt.replace(/u/g, "\\u");
const Ps = "(?:(?![A-Z0-9 $%*+\\-./:]|" + wt + `)(?:.|[\r
]))+`;
R.KANJI = new RegExp(wt, "g");
R.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
R.BYTE = new RegExp(Ps, "g");
R.NUMERIC = new RegExp(je, "g");
R.ALPHANUMERIC = new RegExp(Ss, "g");
const Ns = new RegExp("^" + wt + "$"), Ds = new RegExp("^" + je + "$"), Ms = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
R.testKanji = function(t) {
  return Ns.test(t);
};
R.testNumeric = function(t) {
  return Ds.test(t);
};
R.testAlphanumeric = function(t) {
  return Ms.test(t);
};
(function(n) {
  const t = ne, e = R;
  n.NUMERIC = {
    id: "Numeric",
    bit: 1,
    ccBits: [10, 12, 14]
  }, n.ALPHANUMERIC = {
    id: "Alphanumeric",
    bit: 2,
    ccBits: [9, 11, 13]
  }, n.BYTE = {
    id: "Byte",
    bit: 4,
    ccBits: [8, 16, 16]
  }, n.KANJI = {
    id: "Kanji",
    bit: 8,
    ccBits: [8, 10, 12]
  }, n.MIXED = {
    bit: -1
  }, n.getCharCountIndicator = function(r, o) {
    if (!r.ccBits) throw new Error("Invalid mode: " + r);
    if (!t.isValid(o))
      throw new Error("Invalid version: " + o);
    return o >= 1 && o < 10 ? r.ccBits[0] : o < 27 ? r.ccBits[1] : r.ccBits[2];
  }, n.getBestModeForData = function(r) {
    return e.testNumeric(r) ? n.NUMERIC : e.testAlphanumeric(r) ? n.ALPHANUMERIC : e.testKanji(r) ? n.KANJI : n.BYTE;
  }, n.toString = function(r) {
    if (r && r.id) return r.id;
    throw new Error("Invalid mode");
  }, n.isValid = function(r) {
    return r && r.bit && r.ccBits;
  };
  function i(s) {
    if (typeof s != "string")
      throw new Error("Param is not a string");
    switch (s.toLowerCase()) {
      case "numeric":
        return n.NUMERIC;
      case "alphanumeric":
        return n.ALPHANUMERIC;
      case "kanji":
        return n.KANJI;
      case "byte":
        return n.BYTE;
      default:
        throw new Error("Unknown mode: " + s);
    }
  }
  n.from = function(r, o) {
    if (n.isValid(r))
      return r;
    try {
      return i(r);
    } catch {
      return o;
    }
  };
})(W);
(function(n) {
  const t = N, e = xt, i = It, s = W, r = ne, o = 7973, c = t.getBCHDigit(o);
  function a(f, h, g) {
    for (let v = 1; v <= 40; v++)
      if (h <= n.getCapacity(v, g, f))
        return v;
  }
  function l(f, h) {
    return s.getCharCountIndicator(f, h) + 4;
  }
  function d(f, h) {
    let g = 0;
    return f.forEach(function(v) {
      const k = l(v.mode, h);
      g += k + v.getBitsLength();
    }), g;
  }
  function u(f, h) {
    for (let g = 1; g <= 40; g++)
      if (d(f, g) <= n.getCapacity(g, h, s.MIXED))
        return g;
  }
  n.from = function(h, g) {
    return r.isValid(h) ? parseInt(h, 10) : g;
  }, n.getCapacity = function(h, g, v) {
    if (!r.isValid(h))
      throw new Error("Invalid QR Code version");
    typeof v > "u" && (v = s.BYTE);
    const k = t.getSymbolTotalCodewords(h), m = e.getTotalCodewordsCount(h, g), b = (k - m) * 8;
    if (v === s.MIXED) return b;
    const _ = b - l(v, h);
    switch (v) {
      case s.NUMERIC:
        return Math.floor(_ / 10 * 3);
      case s.ALPHANUMERIC:
        return Math.floor(_ / 11 * 2);
      case s.KANJI:
        return Math.floor(_ / 13);
      case s.BYTE:
      default:
        return Math.floor(_ / 8);
    }
  }, n.getBestVersionForData = function(h, g) {
    let v;
    const k = i.from(g, i.M);
    if (Array.isArray(h)) {
      if (h.length > 1)
        return u(h, k);
      if (h.length === 0)
        return 1;
      v = h[0];
    } else
      v = h;
    return a(v.mode, v.getLength(), k);
  }, n.getEncodedBits = function(h) {
    if (!r.isValid(h) || h < 7)
      throw new Error("Invalid QR Code version");
    let g = h << 12;
    for (; t.getBCHDigit(g) - c >= 0; )
      g ^= o << t.getBCHDigit(g) - c;
    return h << 12 | g;
  };
})(Fe);
var Ve = {};
const qt = N, Ge = 1335, Ts = 21522, ke = qt.getBCHDigit(Ge);
Ve.getEncodedBits = function(t, e) {
  const i = t.bit << 3 | e;
  let s = i << 10;
  for (; qt.getBCHDigit(s) - ke >= 0; )
    s ^= Ge << qt.getBCHDigit(s) - ke;
  return (i << 10 | s) ^ Ts;
};
var Ke = {};
const Is = W;
function rt(n) {
  this.mode = Is.NUMERIC, this.data = n.toString();
}
rt.getBitsLength = function(t) {
  return 10 * Math.floor(t / 3) + (t % 3 ? t % 3 * 3 + 1 : 0);
};
rt.prototype.getLength = function() {
  return this.data.length;
};
rt.prototype.getBitsLength = function() {
  return rt.getBitsLength(this.data.length);
};
rt.prototype.write = function(t) {
  let e, i, s;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    i = this.data.substr(e, 3), s = parseInt(i, 10), t.put(s, 10);
  const r = this.data.length - e;
  r > 0 && (i = this.data.substr(e), s = parseInt(i, 10), t.put(s, r * 3 + 1));
};
var xs = rt;
const Ls = W, Ft = [
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
function ot(n) {
  this.mode = Ls.ALPHANUMERIC, this.data = n;
}
ot.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
ot.prototype.getLength = function() {
  return this.data.length;
};
ot.prototype.getBitsLength = function() {
  return ot.getBitsLength(this.data.length);
};
ot.prototype.write = function(t) {
  let e;
  for (e = 0; e + 2 <= this.data.length; e += 2) {
    let i = Ft.indexOf(this.data[e]) * 45;
    i += Ft.indexOf(this.data[e + 1]), t.put(i, 11);
  }
  this.data.length % 2 && t.put(Ft.indexOf(this.data[e]), 6);
};
var Bs = ot;
const Rs = W;
function at(n) {
  this.mode = Rs.BYTE, typeof n == "string" ? this.data = new TextEncoder().encode(n) : this.data = new Uint8Array(n);
}
at.getBitsLength = function(t) {
  return t * 8;
};
at.prototype.getLength = function() {
  return this.data.length;
};
at.prototype.getBitsLength = function() {
  return at.getBitsLength(this.data.length);
};
at.prototype.write = function(n) {
  for (let t = 0, e = this.data.length; t < e; t++)
    n.put(this.data[t], 8);
};
var Us = at;
const Os = W, zs = N;
function ct(n) {
  this.mode = Os.KANJI, this.data = n;
}
ct.getBitsLength = function(t) {
  return t * 13;
};
ct.prototype.getLength = function() {
  return this.data.length;
};
ct.prototype.getBitsLength = function() {
  return ct.getBitsLength(this.data.length);
};
ct.prototype.write = function(n) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let e = zs.toSJIS(this.data[t]);
    if (e >= 33088 && e <= 40956)
      e -= 33088;
    else if (e >= 57408 && e <= 60351)
      e -= 49472;
    else
      throw new Error(
        "Invalid SJIS character: " + this.data[t] + `
Make sure your charset is UTF-8`
      );
    e = (e >>> 8 & 255) * 192 + (e & 255), n.put(e, 13);
  }
};
var Hs = ct, qe = { exports: {} };
(function(n) {
  var t = {
    single_source_shortest_paths: function(e, i, s) {
      var r = {}, o = {};
      o[i] = 0;
      var c = t.PriorityQueue.make();
      c.push(i, 0);
      for (var a, l, d, u, f, h, g, v, k; !c.empty(); ) {
        a = c.pop(), l = a.value, u = a.cost, f = e[l] || {};
        for (d in f)
          f.hasOwnProperty(d) && (h = f[d], g = u + h, v = o[d], k = typeof o[d] > "u", (k || v > g) && (o[d] = g, c.push(d, g), r[d] = l));
      }
      if (typeof s < "u" && typeof o[s] > "u") {
        var m = ["Could not find a path from ", i, " to ", s, "."].join("");
        throw new Error(m);
      }
      return r;
    },
    extract_shortest_path_from_predecessor_list: function(e, i) {
      for (var s = [], r = i; r; )
        s.push(r), e[r], r = e[r];
      return s.reverse(), s;
    },
    find_path: function(e, i, s) {
      var r = t.single_source_shortest_paths(e, i, s);
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
        var i = t.PriorityQueue, s = {}, r;
        e = e || {};
        for (r in i)
          i.hasOwnProperty(r) && (s[r] = i[r]);
        return s.queue = [], s.sorter = e.sorter || i.default_sorter, s;
      },
      default_sorter: function(e, i) {
        return e.cost - i.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(e, i) {
        var s = { value: e, cost: i };
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
  n.exports = t;
})(qe);
var Fs = qe.exports;
(function(n) {
  const t = W, e = xs, i = Bs, s = Us, r = Hs, o = R, c = N, a = Fs;
  function l(m) {
    return unescape(encodeURIComponent(m)).length;
  }
  function d(m, b, _) {
    const p = [];
    let E;
    for (; (E = m.exec(_)) !== null; )
      p.push({
        data: E[0],
        index: E.index,
        mode: b,
        length: E[0].length
      });
    return p;
  }
  function u(m) {
    const b = d(o.NUMERIC, t.NUMERIC, m), _ = d(o.ALPHANUMERIC, t.ALPHANUMERIC, m);
    let p, E;
    return c.isKanjiModeEnabled() ? (p = d(o.BYTE, t.BYTE, m), E = d(o.KANJI, t.KANJI, m)) : (p = d(o.BYTE_KANJI, t.BYTE, m), E = []), b.concat(_, p, E).sort(function(A, x) {
      return A.index - x.index;
    }).map(function(A) {
      return {
        data: A.data,
        mode: A.mode,
        length: A.length
      };
    });
  }
  function f(m, b) {
    switch (b) {
      case t.NUMERIC:
        return e.getBitsLength(m);
      case t.ALPHANUMERIC:
        return i.getBitsLength(m);
      case t.KANJI:
        return r.getBitsLength(m);
      case t.BYTE:
        return s.getBitsLength(m);
    }
  }
  function h(m) {
    return m.reduce(function(b, _) {
      const p = b.length - 1 >= 0 ? b[b.length - 1] : null;
      return p && p.mode === _.mode ? (b[b.length - 1].data += _.data, b) : (b.push(_), b);
    }, []);
  }
  function g(m) {
    const b = [];
    for (let _ = 0; _ < m.length; _++) {
      const p = m[_];
      switch (p.mode) {
        case t.NUMERIC:
          b.push([
            p,
            { data: p.data, mode: t.ALPHANUMERIC, length: p.length },
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          b.push([
            p,
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.KANJI:
          b.push([
            p,
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
          break;
        case t.BYTE:
          b.push([
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
      }
    }
    return b;
  }
  function v(m, b) {
    const _ = {}, p = { start: {} };
    let E = ["start"];
    for (let $ = 0; $ < m.length; $++) {
      const A = m[$], x = [];
      for (let V = 0; V < A.length; V++) {
        const B = A[V], dt = "" + $ + V;
        x.push(dt), _[dt] = { node: B, lastCount: 0 }, p[dt] = {};
        for (let Rt = 0; Rt < E.length; Rt++) {
          const U = E[Rt];
          _[U] && _[U].node.mode === B.mode ? (p[U][dt] = f(_[U].lastCount + B.length, B.mode) - f(_[U].lastCount, B.mode), _[U].lastCount += B.length) : (_[U] && (_[U].lastCount = B.length), p[U][dt] = f(B.length, B.mode) + 4 + t.getCharCountIndicator(B.mode, b));
        }
      }
      E = x;
    }
    for (let $ = 0; $ < E.length; $++)
      p[E[$]].end = 0;
    return { map: p, table: _ };
  }
  function k(m, b) {
    let _;
    const p = t.getBestModeForData(m);
    if (_ = t.from(b, p), _ !== t.BYTE && _.bit < p.bit)
      throw new Error('"' + m + '" cannot be encoded with mode ' + t.toString(_) + `.
 Suggested mode is: ` + t.toString(p));
    switch (_ === t.KANJI && !c.isKanjiModeEnabled() && (_ = t.BYTE), _) {
      case t.NUMERIC:
        return new e(m);
      case t.ALPHANUMERIC:
        return new i(m);
      case t.KANJI:
        return new r(m);
      case t.BYTE:
        return new s(m);
    }
  }
  n.fromArray = function(b) {
    return b.reduce(function(_, p) {
      return typeof p == "string" ? _.push(k(p, null)) : p.data && _.push(k(p.data, p.mode)), _;
    }, []);
  }, n.fromString = function(b, _) {
    const p = u(b, c.isKanjiModeEnabled()), E = g(p), $ = v(E, _), A = a.find_path($.map, "start", "end"), x = [];
    for (let V = 1; V < A.length - 1; V++)
      x.push($.table[A[V]].node);
    return n.fromArray(h(x));
  }, n.rawSplit = function(b) {
    return n.fromArray(
      u(b, c.isKanjiModeEnabled())
    );
  };
})(Ke);
const Bt = N, jt = It, js = $s, Vs = As, Gs = Re, Ks = Ue, Jt = Oe, Wt = xt, qs = ks, Dt = Fe, Js = Ve, Ws = W, Vt = Ke;
function Ys(n, t) {
  const e = n.size, i = Ks.getPositions(t);
  for (let s = 0; s < i.length; s++) {
    const r = i[s][0], o = i[s][1];
    for (let c = -1; c <= 7; c++)
      if (!(r + c <= -1 || e <= r + c))
        for (let a = -1; a <= 7; a++)
          o + a <= -1 || e <= o + a || (c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 2 && c <= 4 && a >= 2 && a <= 4 ? n.set(r + c, o + a, !0, !0) : n.set(r + c, o + a, !1, !0));
  }
}
function Qs(n) {
  const t = n.size;
  for (let e = 8; e < t - 8; e++) {
    const i = e % 2 === 0;
    n.set(e, 6, i, !0), n.set(6, e, i, !0);
  }
}
function Zs(n, t) {
  const e = Gs.getPositions(t);
  for (let i = 0; i < e.length; i++) {
    const s = e[i][0], r = e[i][1];
    for (let o = -2; o <= 2; o++)
      for (let c = -2; c <= 2; c++)
        o === -2 || o === 2 || c === -2 || c === 2 || o === 0 && c === 0 ? n.set(s + o, r + c, !0, !0) : n.set(s + o, r + c, !1, !0);
  }
}
function Xs(n, t) {
  const e = n.size, i = Dt.getEncodedBits(t);
  let s, r, o;
  for (let c = 0; c < 18; c++)
    s = Math.floor(c / 3), r = c % 3 + e - 8 - 3, o = (i >> c & 1) === 1, n.set(s, r, o, !0), n.set(r, s, o, !0);
}
function Gt(n, t, e) {
  const i = n.size, s = Js.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (s >> r & 1) === 1, r < 6 ? n.set(r, 8, o, !0) : r < 8 ? n.set(r + 1, 8, o, !0) : n.set(i - 15 + r, 8, o, !0), r < 8 ? n.set(8, i - r - 1, o, !0) : r < 9 ? n.set(8, 15 - r - 1 + 1, o, !0) : n.set(8, 15 - r - 1, o, !0);
  n.set(i - 8, 8, 1, !0);
}
function ti(n, t) {
  const e = n.size;
  let i = -1, s = e - 1, r = 7, o = 0;
  for (let c = e - 1; c > 0; c -= 2)
    for (c === 6 && c--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!n.isReserved(s, c - a)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), n.set(s, c - a, l), r--, r === -1 && (o++, r = 7);
        }
      if (s += i, s < 0 || e <= s) {
        s -= i, i = -i;
        break;
      }
    }
}
function ei(n, t, e) {
  const i = new js();
  e.forEach(function(a) {
    i.put(a.mode.bit, 4), i.put(a.getLength(), Ws.getCharCountIndicator(a.mode, n)), a.write(i);
  });
  const s = Bt.getSymbolTotalCodewords(n), r = Wt.getTotalCodewordsCount(n, t), o = (s - r) * 8;
  for (i.getLengthInBits() + 4 <= o && i.put(0, 4); i.getLengthInBits() % 8 !== 0; )
    i.putBit(0);
  const c = (o - i.getLengthInBits()) / 8;
  for (let a = 0; a < c; a++)
    i.put(a % 2 ? 17 : 236, 8);
  return si(i, n, t);
}
function si(n, t, e) {
  const i = Bt.getSymbolTotalCodewords(t), s = Wt.getTotalCodewordsCount(t, e), r = i - s, o = Wt.getBlocksCount(t, e), c = i % o, a = o - c, l = Math.floor(i / o), d = Math.floor(r / o), u = d + 1, f = l - d, h = new qs(f);
  let g = 0;
  const v = new Array(o), k = new Array(o);
  let m = 0;
  const b = new Uint8Array(n.buffer);
  for (let A = 0; A < o; A++) {
    const x = A < a ? d : u;
    v[A] = b.slice(g, g + x), k[A] = h.encode(v[A]), g += x, m = Math.max(m, x);
  }
  const _ = new Uint8Array(i);
  let p = 0, E, $;
  for (E = 0; E < m; E++)
    for ($ = 0; $ < o; $++)
      E < v[$].length && (_[p++] = v[$][E]);
  for (E = 0; E < f; E++)
    for ($ = 0; $ < o; $++)
      _[p++] = k[$][E];
  return _;
}
function ii(n, t, e, i) {
  let s;
  if (Array.isArray(n))
    s = Vt.fromArray(n);
  else if (typeof n == "string") {
    let l = t;
    if (!l) {
      const d = Vt.rawSplit(n);
      l = Dt.getBestVersionForData(d, e);
    }
    s = Vt.fromString(n, l || 40);
  } else
    throw new Error("Invalid data");
  const r = Dt.getBestVersionForData(s, e);
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
  const o = ei(t, e, s), c = Bt.getSymbolSize(t), a = new Vs(c);
  return Ys(a, t), Qs(a), Zs(a, t), Gt(a, e, 0), t >= 7 && Xs(a, t), ti(a, o), isNaN(i) && (i = Jt.getBestMask(
    a,
    Gt.bind(null, a, e)
  )), Jt.applyMask(i, a), Gt(a, e, i), {
    modules: a,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: i,
    segments: s
  };
}
Le.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let i = jt.M, s, r;
  return typeof e < "u" && (i = jt.from(e.errorCorrectionLevel, jt.M), s = Dt.from(e.version), r = Jt.from(e.maskPattern), e.toSJISFunc && Bt.setToSJISFunction(e.toSJISFunc)), ii(t, s, i, r);
};
var Je = {}, re = {};
(function(n) {
  function t(e) {
    if (typeof e == "number" && (e = e.toString()), typeof e != "string")
      throw new Error("Color should be defined as hex string");
    let i = e.slice().replace("#", "").split("");
    if (i.length < 3 || i.length === 5 || i.length > 8)
      throw new Error("Invalid hex color: " + e);
    (i.length === 3 || i.length === 4) && (i = Array.prototype.concat.apply([], i.map(function(r) {
      return [r, r];
    }))), i.length === 6 && i.push("F", "F");
    const s = parseInt(i.join(""), 16);
    return {
      r: s >> 24 & 255,
      g: s >> 16 & 255,
      b: s >> 8 & 255,
      a: s & 255,
      hex: "#" + i.slice(0, 6).join("")
    };
  }
  n.getOptions = function(i) {
    i || (i = {}), i.color || (i.color = {});
    const s = typeof i.margin > "u" || i.margin === null || i.margin < 0 ? 4 : i.margin, r = i.width && i.width >= 21 ? i.width : void 0, o = i.scale || 4;
    return {
      width: r,
      scale: r ? 4 : o,
      margin: s,
      color: {
        dark: t(i.color.dark || "#000000ff"),
        light: t(i.color.light || "#ffffffff")
      },
      type: i.type,
      rendererOpts: i.rendererOpts || {}
    };
  }, n.getScale = function(i, s) {
    return s.width && s.width >= i + s.margin * 2 ? s.width / (i + s.margin * 2) : s.scale;
  }, n.getImageWidth = function(i, s) {
    const r = n.getScale(i, s);
    return Math.floor((i + s.margin * 2) * r);
  }, n.qrToImageData = function(i, s, r) {
    const o = s.modules.size, c = s.modules.data, a = n.getScale(o, r), l = Math.floor((o + r.margin * 2) * a), d = r.margin * a, u = [r.color.light, r.color.dark];
    for (let f = 0; f < l; f++)
      for (let h = 0; h < l; h++) {
        let g = (f * l + h) * 4, v = r.color.light;
        if (f >= d && h >= d && f < l - d && h < l - d) {
          const k = Math.floor((f - d) / a), m = Math.floor((h - d) / a);
          v = u[c[k * o + m] ? 1 : 0];
        }
        i[g++] = v.r, i[g++] = v.g, i[g++] = v.b, i[g] = v.a;
      }
  };
})(re);
(function(n) {
  const t = re;
  function e(s, r, o) {
    s.clearRect(0, 0, r.width, r.height), r.style || (r.style = {}), r.height = o, r.width = o, r.style.height = o + "px", r.style.width = o + "px";
  }
  function i() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  n.render = function(r, o, c) {
    let a = c, l = o;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), o || (l = i()), a = t.getOptions(a);
    const d = t.getImageWidth(r.modules.size, a), u = l.getContext("2d"), f = u.createImageData(d, d);
    return t.qrToImageData(f.data, r, a), e(u, l, d), u.putImageData(f, 0, 0), l;
  }, n.renderToDataURL = function(r, o, c) {
    let a = c;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), a || (a = {});
    const l = n.render(r, o, a), d = a.type || "image/png", u = a.rendererOpts || {};
    return l.toDataURL(d, u.quality);
  };
})(Je);
var We = {};
const ni = re;
function Se(n, t) {
  const e = n.a / 255, i = t + '="' + n.hex + '"';
  return e < 1 ? i + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : i;
}
function Kt(n, t, e) {
  let i = n + t;
  return typeof e < "u" && (i += " " + e), i;
}
function ri(n, t, e) {
  let i = "", s = 0, r = !1, o = 0;
  for (let c = 0; c < n.length; c++) {
    const a = Math.floor(c % t), l = Math.floor(c / t);
    !a && !r && (r = !0), n[c] ? (o++, c > 0 && a > 0 && n[c - 1] || (i += r ? Kt("M", a + e, 0.5 + l + e) : Kt("m", s, 0), s = 0, r = !1), a + 1 < t && n[c + 1] || (i += Kt("h", o), o = 0)) : s++;
  }
  return i;
}
We.render = function(t, e, i) {
  const s = ni.getOptions(e), r = t.modules.size, o = t.modules.data, c = r + s.margin * 2, a = s.color.light.a ? "<path " + Se(s.color.light, "fill") + ' d="M0 0h' + c + "v" + c + 'H0z"/>' : "", l = "<path " + Se(s.color.dark, "stroke") + ' d="' + ri(o, r, s.margin) + '"/>', d = 'viewBox="0 0 ' + c + " " + c + '"', f = '<svg xmlns="http://www.w3.org/2000/svg" ' + (s.width ? 'width="' + s.width + '" height="' + s.width + '" ' : "") + d + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof i == "function" && i(null, f), f;
};
const oi = bs, Yt = Le, Ye = Je, ai = We;
function oe(n, t, e, i, s) {
  const r = [].slice.call(arguments, 1), o = r.length, c = typeof r[o - 1] == "function";
  if (!c && !oi())
    throw new Error("Callback required as last argument");
  if (c) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (s = e, e = t, t = i = void 0) : o === 3 && (t.getContext && typeof s > "u" ? (s = i, i = void 0) : (s = i, i = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = i = void 0) : o === 2 && !t.getContext && (i = e, e = t, t = void 0), new Promise(function(a, l) {
      try {
        const d = Yt.create(e, i);
        a(n(d, t, i));
      } catch (d) {
        l(d);
      }
    });
  }
  try {
    const a = Yt.create(e, i);
    s(null, n(a, t, i));
  } catch (a) {
    s(a);
  }
}
Et.create = Yt.create;
Et.toCanvas = oe.bind(null, Ye.render);
Et.toDataURL = oe.bind(null, Ye.renderToDataURL);
Et.toString = oe.bind(null, function(n, t, e) {
  return ai.render(n, e);
});
var ci = Object.defineProperty, M = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && ci(t, e, s), s;
};
const le = class le extends D {
  constructor() {
    super(...arguments), this._networks = [], this._ssids = [], this._isLoading = !0, this._loadingMessage = "Connecting...", this._computeLabel = (t) => t.name === "networkId" ? "Network (Optional filter)" : t.name === "ssid" ? "SSID (Required)" : t.name === "password" ? "Password (Optional override or Entity ID)" : t.name === "name" ? "Card Title (Optional)" : t.name;
  }
  setConfig(t) {
    this._config = t;
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    if (!this.hass) return;
    const { networks: t, ssids: e } = await P.pollConfig(
      this.hass,
      (i, s) => {
        this._loadingMessage = i, this._isLoading = s;
      }
    );
    this._networks = t, this._ssids = e;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = t.detail.value, i = { ...this._config, ...e };
    this._config.networkId !== e.networkId && (i.ssid = ""), Object.keys(i).forEach((s) => {
      i[s] === "" && delete i[s];
    }), this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: i }, bubbles: !0, composed: !0 }));
  }
  render() {
    if (!this.hass || !this._config) return w``;
    if (this._isLoading)
      return w`
        <div class="editor-container">
          <ha-circular-progress active></ha-circular-progress>
          <div style="margin-top: 16px; color: var(--secondary-text-color);">
            ${this._loadingMessage}
          </div>
        </div>
      `;
    const t = P.getNetworkOptions(this._networks, !0), e = P.getSsidOptions(this._ssids, this._config.networkId, "name"), i = [
      { name: "networkId", selector: { select: { options: t, mode: "dropdown" } } },
      { name: "ssid", selector: { select: { options: e, custom_value: !0, mode: "dropdown" } } },
      { name: "password", selector: { text: {} } },
      { name: "name", selector: { text: {} } }
    ];
    return w`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${i}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
};
le.styles = F`.editor-container { padding: 16px; }`;
let z = le;
M([
  j({ attribute: !1 })
], z.prototype, "hass");
M([
  y()
], z.prototype, "_config");
M([
  y()
], z.prototype, "_networks");
M([
  y()
], z.prototype, "_ssids");
M([
  y()
], z.prototype, "_isLoading");
M([
  y()
], z.prototype, "_loadingMessage");
const de = class de extends D {
  constructor() {
    super(...arguments), this._qrSvg = "", this._isLoading = !0, this._loadingMessage = "Connecting...", this._ssids = [];
  }
  static async getConfigElement() {
    return document.createElement("meraki-wifi-qr-card-editor");
  }
  setConfig(t) {
    if (!t || !t.ssid)
      throw new Error("Please select an SSID");
    this._config = t;
  }
  static getStubConfig() {
    return {
      ssid: "",
      name: "Wi-Fi Access"
    };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    if (!this.hass) return;
    const { ssids: t } = await P.pollConfig(
      this.hass,
      (e, i) => {
        this._loadingMessage = e, this._isLoading = i;
      }
    );
    this._ssids = t, this._generateQR();
  }
  updated(t) {
    (t.has("hass") || t.has("_config")) && this._generateQR();
  }
  _getValue(t) {
    return !t || !this.hass ? t || "" : this.hass.states[t] ? this.hass.states[t].state : t;
  }
  _getPasswordForSsid(t) {
    var r, o;
    if (!this.hass) return "";
    if ((r = this._config) != null && r.password && this._config.password !== "password123")
      return this._getValue(this._config.password);
    if (!t) return "";
    const e = (o = this._config) == null ? void 0 : o.networkId, i = this._ssids.find(
      (c) => c.name === t && (!e || c.networkId === e)
    );
    if (i)
      for (const c in this.hass.states) {
        const a = this.hass.states[c], l = a.attributes;
        if (l.network_id === i.networkId && l.ssid_number === i.number) {
          if (l.psk) return String(l.psk);
          if (l.password) return String(l.password);
          if (a.state && !["unknown", "unavailable"].includes(a.state) && (c.includes("password") || c.includes("psk")))
            return a.state;
        }
      }
    const s = t.toLowerCase().replace(/[^a-z0-9]/g, "_");
    for (const c in this.hass.states)
      if (c.includes(s) && (c.includes("password") || c.includes("psk"))) {
        const a = this.hass.states[c];
        if (a.state && !["unknown", "unavailable"].includes(a.state))
          return a.state;
      }
    return "";
  }
  _generateWifiString(t, e) {
    const i = t.replace(/([\\;,":])/g, "\\$1"), s = e ? e.replace(/([\\;,":])/g, "\\$1") : "";
    return s ? `WIFI:T:WPA;S:${i};P:${s};;` : `WIFI:T:nopass;S:${i};P:;;`;
  }
  async _generateQR() {
    if (!this._config) return;
    const t = this._getValue(this._config.ssid), e = this._getPasswordForSsid(t);
    if (!t) {
      this._qrSvg = "";
      return;
    }
    try {
      const i = this._generateWifiString(t, e);
      this._qrSvg = await Et.toString(i, {
        type: "svg",
        margin: 2,
        color: { dark: "#000000", light: "#ffffff" }
      });
    } catch (i) {
      console.error("Failed to generate QR code", i), this._qrSvg = "";
    }
  }
  render() {
    var i;
    if (!this._config || !this.hass) return w``;
    if (this._isLoading)
      return w`
        <ha-card .header=${((i = this._config) == null ? void 0 : i.name) || "Wi-Fi Access"}>
          <div class="card-content" style="text-align: center; padding: 32px;">
            <ha-circular-progress active></ha-circular-progress>
            <div style="margin-top: 16px; color: var(--secondary-text-color);">
              ${this._loadingMessage}
            </div>
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    const t = this._getValue(this._config.ssid), e = this._getPasswordForSsid(t);
    return w`
      <ha-card .header=${this._config.name || "Wi-Fi Access"}>
        <div class="card-content">
          <div class="ssid-display">${t}</div>
          <div class="qr-container" .innerHTML=${this._qrSvg}></div>
          ${e ? w`<div class="password-display">Password: <code>${e}</code></div>` : ""}
        </div>
        <div class="version">v${"2.3.0-beta.3501"}</div>
      </ha-card>
    `;
  }
};
de.styles = [
  Tt,
  F`
      :host { display: block; }
      .card-content { display: flex; flex-direction: column; align-items: center; padding: 16px; gap: 16px; }
      .ssid-display { font-size: 1.5em; font-weight: bold; color: var(--primary-text-color); text-align: center; }
      .qr-container { width: 200px; height: 200px; background: white; padding: 8px; border-radius: 8px; }
      .qr-container svg { width: 100%; height: 100%; }
      .password-display { color: var(--secondary-text-color); text-align: center; }
      code { background: var(--secondary-background-color); padding: 2px 4px; border-radius: 4px; font-family: monospace; }
    `
];
let H = de;
M([
  j({ attribute: !1 })
], H.prototype, "hass");
M([
  y()
], H.prototype, "_config");
M([
  y()
], H.prototype, "_qrSvg");
M([
  y()
], H.prototype, "_isLoading");
M([
  y()
], H.prototype, "_loadingMessage");
M([
  y()
], H.prototype, "_ssids");
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", H);
customElements.get("meraki-wifi-qr-card-editor") || customElements.define("meraki-wifi-qr-card-editor", z);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-wifi-qr-card") || window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var li = Object.defineProperty, lt = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && li(t, e, s), s;
};
const he = class he extends D {
  constructor() {
    super(...arguments), this._isLoading = !0, this._loadingMessage = "Connecting...";
  }
  static async getConfigElement() {
    return document.createElement("meraki-network-vitals-card-editor");
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = {
      ...t,
      gateway_tap_action: t.gateway_tap_action || { action: "more-info" },
      switch_tap_action: t.switch_tap_action || { action: "more-info" },
      ap_tap_action: t.ap_tap_action || { action: "more-info" }
    };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    this.hass && await P.pollConfig(
      this.hass,
      (t, e) => {
        this._loadingMessage = t, this._isLoading = e;
      }
    );
  }
  static getStubConfig() {
    return {
      gateway_entity: "",
      switch_entity: "",
      ap_entity: "",
      throughput_entity: "sensor.speedtest_download",
      name: "Meraki Network Vitals",
      gateway_tap_action: { action: "more-info" },
      switch_tap_action: { action: "more-info" },
      ap_tap_action: { action: "more-info" }
    };
  }
  _handleEntityClick(t, e) {
    if (!(!t || !e))
      if (e.action === "navigate" && e.navigation_path) {
        const i = new CustomEvent("navigate", {
          detail: { path: e.navigation_path },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(i);
      } else {
        const i = new CustomEvent("hass-more-info", {
          detail: { entityId: t },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(i);
      }
  }
  _renderStatusDot(t, e, i) {
    const s = !!t && !!this.hass.states[t];
    if (!t || !this.hass.states[t])
      return w`
        <div class="status-item">
          <svg height="12" width="12">
            <circle cx="6" cy="6" r="6" fill="var(--disabled-text-color)" />
          </svg>
          <span class="status-label">${e}</span>
        </div>
      `;
    const r = this.hass.states[t];
    console.log(
      `MERAKI CARD DIAGNOSTIC - Status Dot (${e}) Raw Entity State:`,
      r
    );
    const o = r ? r.state.toLowerCase() : "unknown";
    let c = "var(--disabled-text-color)";
    return o === "ok" || o === "online" || o === "connected" ? c = "var(--success-color)" : o === "warning" ? c = "var(--warning-color)" : (o === "error" || o === "offline" || o === "failed") && (c = "var(--error-color)"), w`
      <div
        class="status-item ${s ? "clickable" : ""}"
        @click="${() => s ? this._handleEntityClick(t, i) : null}"
        role="${s ? "button" : "presentation"}"
        tabindex="${s ? "0" : "-1"}"
      >
        <ha-state-icon
          .hass=${this.hass}
          .stateObj=${r}
          class="status-icon"
        ></ha-state-icon>
        <svg height="12" width="12">
          <circle cx="6" cy="6" r="6" fill="${c}" />
        </svg>
        <span class="status-label">${e}</span>
      </div>
    `;
  }
  render() {
    var s;
    if (!this._config || !this.hass)
      return w``;
    if (this._isLoading)
      return w`
        <ha-card>
          <div class="card-content" style="text-align: center; padding: 16px;">
            <ha-circular-progress active size="small"></ha-circular-progress>
            <div style="margin-top: 8px; font-size: 12px; color: var(--secondary-text-color);">
              ${this._loadingMessage}
            </div>
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    const t = this._config.throughput_entity;
    t && this.hass.states[t] && console.log(
      "MERAKI CARD DIAGNOSTIC - Throughput Raw Entity State:",
      this.hass.states[t]
    );
    const e = t ? this.hass.states[t] : void 0, i = e ? (e.state || "0") + " " + (((s = e.attributes) == null ? void 0 : s.unit_of_measurement) || "") : "N/A";
    return w`
      <ha-card>
        <div class="card-content">
          <div class="vitals-container">
            <div class="status-dots">
              ${this._renderStatusDot(
      this._config.gateway_entity,
      "Gateway",
      this._config.gateway_tap_action
    )}
              ${this._renderStatusDot(
      this._config.switch_entity,
      "Switches",
      this._config.switch_tap_action
    )}
              ${this._renderStatusDot(
      this._config.ap_entity,
      "APs",
      this._config.ap_tap_action
    )}
            </div>
            <div class="throughput-container">
              <ha-icon icon="mdi:swap-vertical"></ha-icon>
              <span class="throughput-value">${i}</span>
            </div>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3501"}</div>
      </ha-card>
    `;
  }
};
he.styles = F`
    :host {
      display: block;
    }
    ha-card {
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .card-content {
      padding: 12px 16px;
    }
    .vitals-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .status-dots {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .status-item {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .status-item.clickable {
      cursor: pointer;
    }
    .status-icon {
      --mdc-icon-size: 16px;
      color: var(--secondary-text-color);
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
      font-weight: 600;
      white-space: nowrap;
    }
    .version {
      font-size: 9px;
      color: var(--secondary-text-color);
      text-align: right;
      padding: 0 12px 4px;
      opacity: 0.4;
    }
  `;
let tt = he;
lt([
  j({ attribute: !1 })
], tt.prototype, "hass");
lt([
  y()
], tt.prototype, "_config");
lt([
  y()
], tt.prototype, "_isLoading");
lt([
  y()
], tt.prototype, "_loadingMessage");
const ue = class ue extends D {
  setConfig(t) {
    this._config = t;
  }
  render() {
    var t, e, i;
    return !this.hass || !this._config ? w`` : w`
      <div class="card-config">
        <ha-textfield
          label="Custom Title"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-entity-picker
          label="Gateway Status"
          .hass=${this.hass}
          .value=${this._config.gateway_entity}
          .configValue=${"gateway_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="Switch Aggregation"
          .hass=${this.hass}
          .value=${this._config.switch_entity}
          .configValue=${"switch_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="AP Aggregation"
          .hass=${this.hass}
          .value=${this._config.ap_entity}
          .configValue=${"ap_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="Throughput Sensor"
          .hass=${this.hass}
          .value=${this._config.throughput_entity}
          .configValue=${"throughput_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-textfield
          label="Gateway Tap Action"
          .value=${((t = this._config.gateway_tap_action) == null ? void 0 : t.action) || "more-info"}
          .configValue=${"gateway_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-textfield
          label="Switch Tap Action"
          .value=${((e = this._config.switch_tap_action) == null ? void 0 : e.action) || "more-info"}
          .configValue=${"switch_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-textfield
          label="AP Tap Action"
          .value=${((i = this._config.ap_tap_action) == null ? void 0 : i.action) || "more-info"}
          .configValue=${"ap_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }
  _valueChanged(t) {
    var o;
    if (!this._config) return;
    const e = t.target, i = e.configValue;
    let s = ((o = t.detail) == null ? void 0 : o.value) ?? e.value;
    i && i.endsWith("_tap_action") && (s.startsWith("/") ? s = { action: "navigate", navigation_path: s } : s = { action: s });
    const r = { ...this._config, [i]: s };
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: r },
        bubbles: !0,
        composed: !0
      })
    );
  }
};
ue.styles = F`
    ha-textfield,
    ha-entity-picker {
      display: block;
      margin-bottom: 16px;
      width: 100%;
    }
  `;
let vt = ue;
lt([
  j({ attribute: !1 })
], vt.prototype, "hass");
lt([
  y()
], vt.prototype, "_config");
customElements.get("meraki-network-vitals-card") || customElements.define("meraki-network-vitals-card", tt);
customElements.get("meraki-network-vitals-card-editor") || customElements.define(
  "meraki-network-vitals-card-editor",
  vt
);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-network-vitals-card"
) || window.customCards.push({
  type: "meraki-network-vitals-card",
  name: "Meraki Network Vitals",
  description: "Compact horizontal health header.",
  preview: !0
});
var di = Object.defineProperty, L = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && di(t, e, s), s;
}, st;
let T = (st = class extends D {
  constructor() {
    super(...arguments), this._formData = {
      network: "",
      ssid: "",
      duration: "60",
      guestName: "",
      groupPolicy: "NONE"
    }, this._networks = [], this._ssids = [], this._groupPolicies = [], this._creating = !1, this._error = null, this._success = null, this._isLoading = !0, this._configEntryId = null, this._computeLabel = (t) => t.name === "network" ? "Network" : t.name === "ssid" ? "SSID" : t.name === "duration" ? "Duration" : t.name === "guestName" ? "Guest Name" : t.name === "groupPolicy" ? "Group Policy" : t.name;
  }
  static async getConfigElement() {
    return document.createElement("meraki-guest-access-card-editor");
  }
  setConfig(t) {
    if (!t) throw new Error("Invalid configuration");
    this._config = t;
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  updated(t) {
    var e;
    super.updated(t), t.has("hass") && this.hass && ((e = this.hass.user) != null && e.name) && !this._formData.guestName && (this._formData = { ...this._formData, guestName: this.hass.user.name });
  }
  async _loadCentralizedData() {
    var r;
    if (!this.hass) return;
    this._isLoading = !0;
    const { networks: t, ssids: e, groupPolicies: i, entryId: s } = await P.fetchConfig(this.hass);
    this._networks = t, this._ssids = e, this._groupPolicies = i || [], this._configEntryId = ((r = this._config) == null ? void 0 : r.config_entry_id) || s, t.length > 0 && !this._formData.network && (this._formData = { ...this._formData, network: t[0].id }), this._isLoading = !1;
  }
  _formValueChanged(t) {
    const e = t.detail.value, i = this._formData.network;
    this._formData = { ...this._formData, ...e }, this._formData.network !== i && (this._formData = { ...this._formData, ssid: "", groupPolicy: "NONE" });
  }
  render() {
    var o, c, a;
    if (this._isLoading)
      return w`
        <ha-card .header="${((o = this._config) == null ? void 0 : o.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            ${ys("Loading...")}
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    if (this._networks.length === 0)
      return w`
        <ha-card .header="${((c = this._config) == null ? void 0 : c.name) || "Meraki Guest Access"}">
          <div class="card-content">
            ${ee(
        "No Wireless Networks",
        "No Meraki wireless networks found. Ensure the integration is configured."
      )}
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    const t = P.getNetworkOptions(
      this._networks
    ), e = P.getSsidOptions(
      this._ssids,
      this._formData.network,
      "number"
    ), i = P.getGroupPolicyOptions(
      this._groupPolicies,
      this._formData.network
    ), s = [
      {
        name: "network",
        selector: { select: { options: t, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: e, mode: "dropdown" } }
      },
      {
        name: "groupPolicy",
        selector: {
          select: { options: i, mode: "dropdown" }
        }
      },
      {
        name: "duration",
        selector: {
          select: {
            options: [
              { value: "60", label: "1 Hour" },
              { value: "1440", label: "24 Hours" }
            ],
            mode: "dropdown"
          }
        }
      },
      { name: "guestName", selector: { text: {} } }
    ], r = this._formData.network && this._formData.ssid;
    return w`
      <ha-card .header="${((a = this._config) == null ? void 0 : a.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? w`<ha-alert
                alert-type="error"
                dismissable
                @alert-dismissed-clicked="${() => this._error = null}"
                >${this._error}</ha-alert
              >` : ""}
          ${this._success ? w`<ha-alert
                alert-type="success"
                dismissable
                @alert-dismissed-clicked="${() => this._success = null}"
                >${this._success}</ha-alert
              >` : ""}

          <div class="form-container">
            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${s}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button
              raised
              .disabled=${this._creating || !r}
              @click=${this._generateAccessKey}
            >
              ${this._creating ? w`<ha-circular-progress
                    active
                    size="small"
                  ></ha-circular-progress>` : "Generate Access Key"}
            </ha-button>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3501"}</div>
      </ha-card>
    `;
  }
  async _generateAccessKey() {
    if (!(!this._formData.network || !this._formData.ssid)) {
      this._creating = !0, this._error = null, this._success = null;
      try {
        const t = {
          network_id: this._formData.network,
          ssid: parseInt(this._formData.ssid, 10),
          duration: parseInt(this._formData.duration, 10)
        };
        this._formData.guestName && (t.guest_name = this._formData.guestName), this._formData.groupPolicy && this._formData.groupPolicy !== "NONE" && (t.group_policy = this._formData.groupPolicy), await this.hass.callService(
          "meraki_ha",
          "generate_guest_access",
          t
        ), this._success = "Guest access key created successfully!";
      } catch (t) {
        this._error = `Failed to create guest key: ${t.message || t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
}, st.styles = [
  Tt,
  F`
      .form-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      ha-button {
        width: 100%;
        margin-top: 8px;
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
    `
], st);
L([
  j({ attribute: !1 })
], T.prototype, "hass");
L([
  y()
], T.prototype, "_config");
L([
  y()
], T.prototype, "_formData");
L([
  y()
], T.prototype, "_networks");
L([
  y()
], T.prototype, "_ssids");
L([
  y()
], T.prototype, "_groupPolicies");
L([
  y()
], T.prototype, "_creating");
L([
  y()
], T.prototype, "_error");
L([
  y()
], T.prototype, "_success");
L([
  y()
], T.prototype, "_isLoading");
L([
  y()
], T.prototype, "_configEntryId");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", T);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-guest-access-card"
) || window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Manage temporary guest WiFi access. Version: 2.3.0-beta.3501",
  preview: !0,
  version: "2.3.0-beta.3501"
});
var hi = Object.defineProperty, I = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && hi(t, e, s), s;
};
const fe = class fe extends D {
  constructor() {
    super(...arguments), this._formData = {
      network: "",
      ssid: "",
      passphrase: "",
      policy: "",
      // Added Policy field
      duration: "60",
      guestName: ""
    }, this._networks = [], this._ssids = [], this._policies = [], this._creating = !1, this._error = null, this._success = null, this._isLoading = !0, this._loadingMessage = "Connecting to Meraki...", this._configEntryId = null, this._computeLabel = (t) => t.name === "network" ? "Network" : t.name === "ssid" ? "SSID" : t.name === "policy" ? "Group Policy (Required)" : t.name === "passphrase" ? "Passphrase / PSK (Auto-discovered)" : t.name === "duration" ? "Duration" : t.name === "guestName" ? "Guest Name" : t.name;
  }
  static async getConfigElement() {
    return document.createElement("meraki-guest-access-card-editor");
  }
  setConfig(t) {
    if (!t) throw new Error("Invalid configuration");
    this._config = t;
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  updated(t) {
    var e;
    super.updated(t), t.has("hass") && this.hass && ((e = this.hass.user) != null && e.name) && !this._formData.guestName && (this._formData = { ...this._formData, guestName: this.hass.user.name });
  }
  async _loadCentralizedData() {
    var l;
    if (!this.hass) return;
    const { networks: t, ssids: e, groupPolicies: i, entryId: s } = await P.pollConfig(
      this.hass,
      (d, u) => {
        this._loadingMessage = d, this._isLoading = u;
      }
    );
    if (t.length === 0) {
      this._isLoading = !1;
      return;
    }
    this._networks = t, this._ssids = e, this._policies = i, this._configEntryId = ((l = this._config) == null ? void 0 : l.config_entry_id) || s;
    let r = this._formData.network, o = this._formData.ssid, c = this._formData.passphrase, a = this._formData.policy;
    if (t.length > 0 && !r && (r = t[0].id), r && !o) {
      const d = e.filter((u) => u.networkId === r);
      d.length > 0 && (o = String(d[0].number));
    }
    if (r && o && !c && (c = this._getPasswordForSelectedSsid(r, o)), r && !a) {
      const d = this._policies.filter((u) => u.networkId === r);
      d.length > 0 && (a = String(d[0].groupPolicyId || d[0].id));
    }
    this._formData = {
      ...this._formData,
      network: r,
      ssid: o,
      passphrase: c,
      policy: a
    }, this._isLoading = !1;
  }
  _getPasswordForSelectedSsid(t, e) {
    if (!this.hass || !t || !e) return "";
    const i = parseInt(e, 10);
    let s = "";
    const r = this._ssids.find(
      (o) => o.networkId === t && o.number === i
    );
    r && (s = r.name);
    for (const o in this.hass.states) {
      const a = this.hass.states[o].attributes;
      if (a.network_id === t && a.ssid_number === i) {
        if (s || (s = a.ssid_name || a.ssid || ""), a.psk) return String(a.psk);
        if (a.password) return String(a.password);
      }
    }
    if (s) {
      const o = s.toLowerCase().replace(/[^a-z0-9]/g, "_");
      for (const c in this.hass.states)
        if (c.includes(o) && (c.includes("password") || c.includes("psk"))) {
          const a = this.hass.states[c];
          if (a.state && !["unknown", "unavailable"].includes(a.state))
            return a.state;
        }
    }
    return "";
  }
  _formValueChanged(t) {
    const e = t.detail.value, i = this._formData.network, s = this._formData.ssid;
    let r = { ...this._formData, ...e };
    if (r.network !== i) {
      r.ssid = "", r.passphrase = "", r.policy = "";
      const o = this._ssids.filter(
        (a) => a.networkId === r.network
      );
      o.length > 0 && (r.ssid = String(o[0].number));
      const c = this._policies.filter((a) => a.networkId === r.network);
      c.length > 0 && (r.policy = String(c[0].groupPolicyId || c[0].id));
    }
    r.ssid && r.ssid !== s && (r.passphrase = this._getPasswordForSelectedSsid(
      r.network,
      r.ssid
    )), this._formData = r;
  }
  render() {
    var o, c, a;
    if (console.debug("Meraki Guest Access Card Render State:", {
      isLoading: this._isLoading,
      networks: this._networks.length,
      ssids: this._ssids.length,
      policies: this._policies.length,
      formData: this._formData
    }), this._isLoading)
      return w`
        <ha-card .header="${((o = this._config) == null ? void 0 : o.name) || "Meraki Guest Access"}">
          <div class="card-content" style="display: flex; flex-direction: column; align-items: center; padding: 32px;">
            <ha-circular-progress active></ha-circular-progress>
            <div style="margin-top: 16px; color: var(--secondary-text-color); text-align: center;">
              ${this._loadingMessage}
            </div>
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    if (this._networks.length === 0)
      return w`
        <ha-card .header="${((c = this._config) == null ? void 0 : c.name) || "Meraki Guest Access"}">
          <div class="card-content">
            ${ee(
        "No Wireless Networks",
        "No Meraki wireless networks found. Ensure the integration is configured."
      )}
          </div>
          <div class="version">v${"2.3.0-beta.3501"}</div>
        </ha-card>
      `;
    const t = P.getNetworkOptions(
      this._networks
    ), e = P.getSsidOptions(
      this._ssids,
      this._formData.network,
      "number"
    ), i = this._policies.filter((l) => l.networkId === this._formData.network).map((l) => ({
      value: String(l.groupPolicyId || l.id),
      label: l.name
    })), s = [
      {
        name: "network",
        selector: { select: { options: t, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: e, mode: "dropdown" } }
      },
      // Only show the policy dropdown if policies successfully loaded for this network
      ...i.length > 0 ? [
        {
          name: "policy",
          selector: {
            select: { options: i, mode: "dropdown" }
          }
        }
      ] : [],
      { name: "passphrase", selector: { text: {} } },
      {
        name: "duration",
        selector: {
          select: {
            options: [
              { value: "15", label: "15 Minutes" },
              { value: "30", label: "30 Minutes" },
              { value: "60", label: "1 Hour" },
              { value: "120", label: "2 Hours" },
              { value: "240", label: "4 Hours" },
              { value: "480", label: "8 Hours" },
              { value: "720", label: "12 Hours" },
              { value: "1440", label: "24 Hours" },
              { value: "2880", label: "48 Hours" },
              { value: "10080", label: "7 Days" }
            ],
            mode: "dropdown"
          }
        }
      },
      { name: "guestName", selector: { text: {} } }
    ], r = this._formData.network && this._formData.ssid && this._formData.policy;
    return w`
      <ha-card .header="${((a = this._config) == null ? void 0 : a.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? w`<ha-alert
                alert-type="error"
                dismissable
                @alert-dismissed-clicked="${() => this._error = null}"
                >${this._error}</ha-alert
              >` : ""}
          ${this._success ? w`<ha-alert
                alert-type="success"
                dismissable
                @alert-dismissed-clicked="${() => this._success = null}"
                >${this._success}</ha-alert
              >` : ""}

          <div class="form-container">
            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${s}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button
              raised
              .disabled=${this._creating || !r}
              @click=${this._generateAccessKey}
            >
              ${this._creating ? w`<ha-circular-progress
                    active
                    size="small"
                  ></ha-circular-progress>` : "Generate Access Key"}
            </ha-button>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3501"}</div>
      </ha-card>
    `;
  }
  async _generateAccessKey() {
    if (!(!this._formData.network || !this._formData.ssid || !this._formData.policy)) {
      this._creating = !0, this._error = null, this._success = null;
      try {
        const t = {
          network_id: this._formData.network,
          ssid: parseInt(this._formData.ssid, 10),
          duration: parseInt(this._formData.duration, 10)
        };
        this._formData.policy && this._formData.policy !== "NONE" && this._formData.policy !== "CREATE" && (t.group_policy = this._formData.policy), this._formData.guestName && (t.guest_name = this._formData.guestName), this._formData.passphrase && (t.passphrase = this._formData.passphrase), await this.hass.callService(
          "meraki_ha",
          "generate_guest_access",
          t
        ), this._success = "Guest access key created successfully!";
      } catch (t) {
        this._error = `Failed to create guest key: ${t.message || t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
fe.styles = [
  Tt,
  F`
      .form-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      ha-button {
        width: 100%;
        margin-top: 8px;
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
    `
];
let S = fe;
I([
  j({ attribute: !1 })
], S.prototype, "hass");
I([
  y()
], S.prototype, "_config");
I([
  y()
], S.prototype, "_formData");
I([
  y()
], S.prototype, "_networks");
I([
  y()
], S.prototype, "_ssids");
I([
  y()
], S.prototype, "_policies");
I([
  y()
], S.prototype, "_creating");
I([
  y()
], S.prototype, "_error");
I([
  y()
], S.prototype, "_success");
I([
  y()
], S.prototype, "_isLoading");
I([
  y()
], S.prototype, "_loadingMessage");
I([
  y()
], S.prototype, "_configEntryId");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", S);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-guest-access-card"
) || window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Manage temporary guest WiFi access. Version: 2.3.0-beta.3501",
  preview: !0,
  version: "2.3.0-beta.3501"
});
export {
  S as MerakiGuestAccessCard
};
