/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const $t = globalThis, Yt = $t.ShadowRoot && ($t.ShadyCSS === void 0 || $t.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Qt = Symbol(), ae = /* @__PURE__ */ new WeakMap();
let Ce = class {
  constructor(t, i, s) {
    if (this._$cssResult$ = !0, s !== Qt) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = i;
  }
  get styleSheet() {
    let t = this.o;
    const i = this.t;
    if (Yt && t === void 0) {
      const s = i !== void 0 && i.length === 1;
      s && (t = ae.get(i)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && ae.set(i, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const ze = (e) => new Ce(typeof e == "string" ? e : e + "", void 0, Qt), F = (e, ...t) => {
  const i = e.length === 1 ? e[0] : t.reduce((s, n, r) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(n) + e[r + 1], e[0]);
  return new Ce(i, e, Qt);
}, je = (e, t) => {
  if (Yt) e.adoptedStyleSheets = t.map((i) => i instanceof CSSStyleSheet ? i : i.styleSheet);
  else for (const i of t) {
    const s = document.createElement("style"), n = $t.litNonce;
    n !== void 0 && s.setAttribute("nonce", n), s.textContent = i.cssText, e.appendChild(s);
  }
}, ce = Yt ? (e) => e : (e) => e instanceof CSSStyleSheet ? ((t) => {
  let i = "";
  for (const s of t.cssRules) i += s.cssText;
  return ze(i);
})(e) : e;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: Ge, defineProperty: Ke, getOwnPropertyDescriptor: qe, getOwnPropertyNames: We, getOwnPropertySymbols: Je, getPrototypeOf: Ye } = Object, V = globalThis, le = V.trustedTypes, Qe = le ? le.emptyScript : "", Rt = V.reactiveElementPolyfillSupport, at = (e, t) => e, St = { toAttribute(e, t) {
  switch (t) {
    case Boolean:
      e = e ? Qe : null;
      break;
    case Object:
    case Array:
      e = e == null ? e : JSON.stringify(e);
  }
  return e;
}, fromAttribute(e, t) {
  let i = e;
  switch (t) {
    case Boolean:
      i = e !== null;
      break;
    case Number:
      i = e === null ? null : Number(e);
      break;
    case Object:
    case Array:
      try {
        i = JSON.parse(e);
      } catch {
        i = null;
      }
  }
  return i;
} }, Zt = (e, t) => !Ge(e, t), he = { attribute: !0, type: String, converter: St, reflect: !1, useDefault: !1, hasChanged: Zt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), V.litPropertyMetadata ?? (V.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let Y = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, i = he) {
    if (i.state && (i.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((i = Object.create(i)).wrapped = !0), this.elementProperties.set(t, i), !i.noAccessor) {
      const s = Symbol(), n = this.getPropertyDescriptor(t, s, i);
      n !== void 0 && Ke(this.prototype, t, n);
    }
  }
  static getPropertyDescriptor(t, i, s) {
    const { get: n, set: r } = qe(this.prototype, t) ?? { get() {
      return this[i];
    }, set(o) {
      this[i] = o;
    } };
    return { get: n, set(o) {
      const c = n == null ? void 0 : n.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, c, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? he;
  }
  static _$Ei() {
    if (this.hasOwnProperty(at("elementProperties"))) return;
    const t = Ye(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(at("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(at("properties"))) {
      const i = this.properties, s = [...We(i), ...Je(i)];
      for (const n of s) this.createProperty(n, i[n]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const i = litPropertyMetadata.get(t);
      if (i !== void 0) for (const [s, n] of i) this.elementProperties.set(s, n);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [i, s] of this.elementProperties) {
      const n = this._$Eu(i, s);
      n !== void 0 && this._$Eh.set(n, i);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const i = [];
    if (Array.isArray(t)) {
      const s = new Set(t.flat(1 / 0).reverse());
      for (const n of s) i.unshift(ce(n));
    } else t !== void 0 && i.push(ce(t));
    return i;
  }
  static _$Eu(t, i) {
    const s = i.attribute;
    return s === !1 ? void 0 : typeof s == "string" ? s : typeof t == "string" ? t.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    var t;
    this._$ES = new Promise((i) => this.enableUpdating = i), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), (t = this.constructor.l) == null || t.forEach((i) => i(this));
  }
  addController(t) {
    var i;
    (this._$EO ?? (this._$EO = /* @__PURE__ */ new Set())).add(t), this.renderRoot !== void 0 && this.isConnected && ((i = t.hostConnected) == null || i.call(t));
  }
  removeController(t) {
    var i;
    (i = this._$EO) == null || i.delete(t);
  }
  _$E_() {
    const t = /* @__PURE__ */ new Map(), i = this.constructor.elementProperties;
    for (const s of i.keys()) this.hasOwnProperty(s) && (t.set(s, this[s]), delete this[s]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return je(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    var t;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$EO) == null || t.forEach((i) => {
      var s;
      return (s = i.hostConnected) == null ? void 0 : s.call(i);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$EO) == null || t.forEach((i) => {
      var s;
      return (s = i.hostDisconnected) == null ? void 0 : s.call(i);
    });
  }
  attributeChangedCallback(t, i, s) {
    this._$AK(t, s);
  }
  _$ET(t, i) {
    var r;
    const s = this.constructor.elementProperties.get(t), n = this.constructor._$Eu(t, s);
    if (n !== void 0 && s.reflect === !0) {
      const o = (((r = s.converter) == null ? void 0 : r.toAttribute) !== void 0 ? s.converter : St).toAttribute(i, s.type);
      this._$Em = t, o == null ? this.removeAttribute(n) : this.setAttribute(n, o), this._$Em = null;
    }
  }
  _$AK(t, i) {
    var r, o;
    const s = this.constructor, n = s._$Eh.get(t);
    if (n !== void 0 && this._$Em !== n) {
      const c = s.getPropertyOptions(n), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((r = c.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? c.converter : St;
      this._$Em = n;
      const l = a.fromAttribute(i, c.type);
      this[n] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(n)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, i, s, n = !1, r) {
    var o;
    if (t !== void 0) {
      const c = this.constructor;
      if (n === !1 && (r = this[t]), s ?? (s = c.getPropertyOptions(t)), !((s.hasChanged ?? Zt)(r, i) || s.useDefault && s.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(c._$Eu(t, s)))) return;
      this.C(t, i, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, i, { useDefault: s, reflect: n, wrapped: r }, o) {
    s && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? i ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || s || (i = void 0), this._$AL.set(t, i)), n === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (i) {
      Promise.reject(i);
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
    const i = this._$AL;
    try {
      t = this.shouldUpdate(i), t ? (this.willUpdate(i), (s = this._$EO) == null || s.forEach((n) => {
        var r;
        return (r = n.hostUpdate) == null ? void 0 : r.call(n);
      }), this.update(i)) : this._$EM();
    } catch (n) {
      throw t = !1, this._$EM(), n;
    }
    t && this._$AE(i);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var i;
    (i = this._$EO) == null || i.forEach((s) => {
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
    this._$Eq && (this._$Eq = this._$Eq.forEach((i) => this._$ET(i, this[i]))), this._$EM();
  }
  updated(t) {
  }
  firstUpdated(t) {
  }
};
Y.elementStyles = [], Y.shadowRootOptions = { mode: "open" }, Y[at("elementProperties")] = /* @__PURE__ */ new Map(), Y[at("finalized")] = /* @__PURE__ */ new Map(), Rt == null || Rt({ ReactiveElement: Y }), (V.reactiveElementVersions ?? (V.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ct = globalThis, ue = (e) => e, At = ct.trustedTypes, de = At ? At.createPolicy("lit-html", { createHTML: (e) => e }) : void 0, be = "$lit$", O = `lit$${Math.random().toFixed(9).slice(2)}$`, $e = "?" + O, Ze = `<${$e}>`, q = document, ht = () => q.createComment(""), ut = (e) => e === null || typeof e != "object" && typeof e != "function", Xt = Array.isArray, Xe = (e) => Xt(e) || typeof (e == null ? void 0 : e[Symbol.iterator]) == "function", Ut = `[
\f\r]`, ot = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, fe = /-->/g, ge = />/g, j = RegExp(`>|${Ut}(?:([^\\s"'>=/]+)(${Ut}*=${Ut}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), pe = /'/g, _e = /"/g, Se = /^(?:script|style|textarea|title)$/i, ti = (e) => (t, ...i) => ({ _$litType$: e, strings: t, values: i }), v = ti(1), Q = Symbol.for("lit-noChange"), A = Symbol.for("lit-nothing"), me = /* @__PURE__ */ new WeakMap(), G = q.createTreeWalker(q, 129);
function Ae(e, t) {
  if (!Xt(e) || !e.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return de !== void 0 ? de.createHTML(t) : t;
}
const ei = (e, t) => {
  const i = e.length - 1, s = [];
  let n, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = ot;
  for (let c = 0; c < i; c++) {
    const a = e[c];
    let l, h, f = -1, d = 0;
    for (; d < a.length && (o.lastIndex = d, h = o.exec(a), h !== null); ) d = o.lastIndex, o === ot ? h[1] === "!--" ? o = fe : h[1] !== void 0 ? o = ge : h[2] !== void 0 ? (Se.test(h[2]) && (n = RegExp("</" + h[2], "g")), o = j) : h[3] !== void 0 && (o = j) : o === j ? h[0] === ">" ? (o = n ?? ot, f = -1) : h[1] === void 0 ? f = -2 : (f = o.lastIndex - h[2].length, l = h[1], o = h[3] === void 0 ? j : h[3] === '"' ? _e : pe) : o === _e || o === pe ? o = j : o === fe || o === ge ? o = ot : (o = j, n = void 0);
    const u = o === j && e[c + 1].startsWith("/>") ? " " : "";
    r += o === ot ? a + Ze : f >= 0 ? (s.push(l), a.slice(0, f) + be + a.slice(f) + O + u) : a + O + (f === -2 ? c : u);
  }
  return [Ae(e, r + (e[i] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class dt {
  constructor({ strings: t, _$litType$: i }, s) {
    let n;
    this.parts = [];
    let r = 0, o = 0;
    const c = t.length - 1, a = this.parts, [l, h] = ei(t, i);
    if (this.el = dt.createElement(l, s), G.currentNode = this.el.content, i === 2 || i === 3) {
      const f = this.el.content.firstChild;
      f.replaceWith(...f.childNodes);
    }
    for (; (n = G.nextNode()) !== null && a.length < c; ) {
      if (n.nodeType === 1) {
        if (n.hasAttributes()) for (const f of n.getAttributeNames()) if (f.endsWith(be)) {
          const d = h[o++], u = n.getAttribute(f).split(O), _ = /([.?@])?(.*)/.exec(d);
          a.push({ type: 1, index: r, name: _[2], strings: u, ctor: _[1] === "." ? ni : _[1] === "?" ? si : _[1] === "@" ? ri : Mt }), n.removeAttribute(f);
        } else f.startsWith(O) && (a.push({ type: 6, index: r }), n.removeAttribute(f));
        if (Se.test(n.tagName)) {
          const f = n.textContent.split(O), d = f.length - 1;
          if (d > 0) {
            n.textContent = At ? At.emptyScript : "";
            for (let u = 0; u < d; u++) n.append(f[u], ht()), G.nextNode(), a.push({ type: 2, index: ++r });
            n.append(f[d], ht());
          }
        }
      } else if (n.nodeType === 8) if (n.data === $e) a.push({ type: 2, index: r });
      else {
        let f = -1;
        for (; (f = n.data.indexOf(O, f + 1)) !== -1; ) a.push({ type: 7, index: r }), f += O.length - 1;
      }
      r++;
    }
  }
  static createElement(t, i) {
    const s = q.createElement("template");
    return s.innerHTML = t, s;
  }
}
function Z(e, t, i = e, s) {
  var o, c;
  if (t === Q) return t;
  let n = s !== void 0 ? (o = i._$Co) == null ? void 0 : o[s] : i._$Cl;
  const r = ut(t) ? void 0 : t._$litDirective$;
  return (n == null ? void 0 : n.constructor) !== r && ((c = n == null ? void 0 : n._$AO) == null || c.call(n, !1), r === void 0 ? n = void 0 : (n = new r(e), n._$AT(e, i, s)), s !== void 0 ? (i._$Co ?? (i._$Co = []))[s] = n : i._$Cl = n), n !== void 0 && (t = Z(e, n._$AS(e, t.values), n, s)), t;
}
class ii {
  constructor(t, i) {
    this._$AV = [], this._$AN = void 0, this._$AD = t, this._$AM = i;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(t) {
    const { el: { content: i }, parts: s } = this._$AD, n = ((t == null ? void 0 : t.creationScope) ?? q).importNode(i, !0);
    G.currentNode = n;
    let r = G.nextNode(), o = 0, c = 0, a = s[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let l;
        a.type === 2 ? l = new wt(r, r.nextSibling, this, t) : a.type === 1 ? l = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (l = new oi(r, this, t)), this._$AV.push(l), a = s[++c];
      }
      o !== (a == null ? void 0 : a.index) && (r = G.nextNode(), o++);
    }
    return G.currentNode = q, n;
  }
  p(t) {
    let i = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, i), i += s.strings.length - 2) : s._$AI(t[i])), i++;
  }
}
class wt {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, i, s, n) {
    this.type = 2, this._$AH = A, this._$AN = void 0, this._$AA = t, this._$AB = i, this._$AM = s, this.options = n, this._$Cv = (n == null ? void 0 : n.isConnected) ?? !0;
  }
  get parentNode() {
    let t = this._$AA.parentNode;
    const i = this._$AM;
    return i !== void 0 && (t == null ? void 0 : t.nodeType) === 11 && (t = i.parentNode), t;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(t, i = this) {
    t = Z(this, t, i), ut(t) ? t === A || t == null || t === "" ? (this._$AH !== A && this._$AR(), this._$AH = A) : t !== this._$AH && t !== Q && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : Xe(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== A && ut(this._$AH) ? this._$AA.nextSibling.data = t : this.T(q.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: i, _$litType$: s } = t, n = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = dt.createElement(Ae(s.h, s.h[0]), this.options)), s);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === n) this._$AH.p(i);
    else {
      const o = new ii(n, this), c = o.u(this.options);
      o.p(i), this.T(c), this._$AH = o;
    }
  }
  _$AC(t) {
    let i = me.get(t.strings);
    return i === void 0 && me.set(t.strings, i = new dt(t)), i;
  }
  k(t) {
    Xt(this._$AH) || (this._$AH = [], this._$AR());
    const i = this._$AH;
    let s, n = 0;
    for (const r of t) n === i.length ? i.push(s = new wt(this.O(ht()), this.O(ht()), this, this.options)) : s = i[n], s._$AI(r), n++;
    n < i.length && (this._$AR(s && s._$AB.nextSibling, n), i.length = n);
  }
  _$AR(t = this._$AA.nextSibling, i) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, i); t !== this._$AB; ) {
      const n = ue(t).nextSibling;
      ue(t).remove(), t = n;
    }
  }
  setConnected(t) {
    var i;
    this._$AM === void 0 && (this._$Cv = t, (i = this._$AP) == null || i.call(this, t));
  }
}
class Mt {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, i, s, n, r) {
    this.type = 1, this._$AH = A, this._$AN = void 0, this.element = t, this.name = i, this._$AM = n, this.options = r, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = A;
  }
  _$AI(t, i = this, s, n) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = Z(this, t, i, 0), o = !ut(t) || t !== this._$AH && t !== Q, o && (this._$AH = t);
    else {
      const c = t;
      let a, l;
      for (t = r[0], a = 0; a < r.length - 1; a++) l = Z(this, c[s + a], i, a), l === Q && (l = this._$AH[a]), o || (o = !ut(l) || l !== this._$AH[a]), l === A ? t = A : t !== A && (t += (l ?? "") + r[a + 1]), this._$AH[a] = l;
    }
    o && !n && this.j(t);
  }
  j(t) {
    t === A ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class ni extends Mt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === A ? void 0 : t;
  }
}
class si extends Mt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== A);
  }
}
class ri extends Mt {
  constructor(t, i, s, n, r) {
    super(t, i, s, n, r), this.type = 5;
  }
  _$AI(t, i = this) {
    if ((t = Z(this, t, i, 0) ?? A) === Q) return;
    const s = this._$AH, n = t === A && s !== A || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, r = t !== A && (s === A || n);
    n && this.element.removeEventListener(this.name, this, s), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var i;
    typeof this._$AH == "function" ? this._$AH.call(((i = this.options) == null ? void 0 : i.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class oi {
  constructor(t, i, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = i, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    Z(this, t);
  }
}
const Lt = ct.litHtmlPolyfillSupport;
Lt == null || Lt(dt, wt), (ct.litHtmlVersions ?? (ct.litHtmlVersions = [])).push("3.3.2");
const ai = (e, t, i) => {
  const s = (i == null ? void 0 : i.renderBefore) ?? t;
  let n = s._$litPart$;
  if (n === void 0) {
    const r = (i == null ? void 0 : i.renderBefore) ?? null;
    s._$litPart$ = n = new wt(t.insertBefore(ht(), r), r, void 0, i ?? {});
  }
  return n._$AI(e), n;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const K = globalThis;
class M extends Y {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    var i;
    const t = super.createRenderRoot();
    return (i = this.renderOptions).renderBefore ?? (i.renderBefore = t.firstChild), t;
  }
  update(t) {
    const i = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = ai(i, this.renderRoot, this.renderOptions);
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
    return Q;
  }
}
var Ee;
M._$litElement$ = !0, M.finalized = !0, (Ee = K.litElementHydrateSupport) == null || Ee.call(K, { LitElement: M });
const Ot = K.litElementPolyfillSupport;
Ot == null || Ot({ LitElement: M });
(K.litElementVersions ?? (K.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const J = (e) => (t, i) => {
  i !== void 0 ? i.addInitializer(() => {
    customElements.define(e, t);
  }) : customElements.define(e, t);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ci = { attribute: !0, type: String, converter: St, reflect: !1, hasChanged: Zt }, li = (e = ci, t, i) => {
  const { kind: s, metadata: n } = i;
  let r = globalThis.litPropertyMetadata.get(n);
  if (r === void 0 && globalThis.litPropertyMetadata.set(n, r = /* @__PURE__ */ new Map()), s === "setter" && ((e = Object.create(e)).wrapped = !0), r.set(i.name, e), s === "accessor") {
    const { name: o } = i;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(o, a, e, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(o, void 0, e, c), c;
    } };
  }
  if (s === "setter") {
    const { name: o } = i;
    return function(c) {
      const a = this[o];
      t.call(this, c), this.requestUpdate(o, a, e, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + s);
};
function U(e) {
  return (t, i) => typeof i == "object" ? li(e, t, i) : ((s, n, r) => {
    const o = n.hasOwnProperty(r);
    return n.constructor.createProperty(r, s), o ? Object.getOwnPropertyDescriptor(n, r) : void 0;
  })(e, t, i);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function E(e) {
  return U({ ...e, state: !0, attribute: !1 });
}
var hi = Object.defineProperty, ui = Object.getOwnPropertyDescriptor, nt = (e, t, i, s) => {
  for (var n = s > 1 ? void 0 : s ? ui(t, i) : t, r = e.length - 1, o; r >= 0; r--)
    (o = e[r]) && (n = (s ? o(t, i, n) : o(n)) || n);
  return s && n && hi(t, i, n), n;
};
let ft = class extends M {
  static async getConfigElement() {
    return document.createElement("meraki-content-filter-card-editor");
  }
  setConfig(e) {
    if (!e || !e.entity)
      throw new Error("Please define a Meraki content filter entity");
    this._config = e;
  }
  static getStubConfig() {
    return {
      entity: "select.meraki_network_content_filter",
      name: "Meraki Content Filter"
    };
  }
  render() {
    if (!this._config || !this.hass)
      return v``;
    const e = this._config.entity, t = this.hass.states[e];
    if (!t)
      return v`
        <ha-card>
          <div class="card-content">
            <ha-alert alert-type="error">Entity not found: ${e}</ha-alert>
          </div>
        </ha-card>
      `;
    const i = t.state, s = t.attributes.options || ["None", "Security", "Family", "Strict"], n = this._config.name || t.attributes.friendly_name || "Content Filter";
    return v`
      <ha-card>
        <div class="card-header">${n}</div>
        <div class="card-content">
          <div class="current-profile">
            Current Profile: <strong>${i}</strong>
          </div>
          <div class="profile-buttons">
            ${s.map((r) => v`
              <div
                class="profile-button ${i === r ? "active" : ""}"
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
  async _handleProfileSelect(e) {
    if (!(!this.hass || !this._config))
      try {
        await this.hass.callService("select", "select_option", {
          entity_id: this._config.entity,
          option: e
        });
      } catch (t) {
        console.error("Failed to call select_option service:", t);
      }
  }
};
ft.styles = F`
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
nt([
  U({ attribute: !1 })
], ft.prototype, "hass", 2);
nt([
  E()
], ft.prototype, "_config", 2);
ft = nt([
  J("meraki-content-filter-card")
], ft);
let gt = class extends M {
  setConfig(e) {
    this._config = e;
  }
  render() {
    return !this.hass || !this._config ? v`` : v`
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
  _valueChanged(e) {
    if (!this._config || !this.hass)
      return;
    const t = e.target, i = t.configValue;
    if (!i)
      return;
    let s = t.value;
    if (this._config[i] === s)
      return;
    const n = { ...this._config };
    s === "" || s === void 0 ? delete n[i] : n[i] = s, this._config = n;
    const r = new CustomEvent("config-changed", {
      detail: { config: this._config },
      bubbles: !0,
      composed: !0
    });
    this.dispatchEvent(r);
  }
};
gt.styles = F`
    .card-config ha-entity-picker,
    .card-config ha-textfield {
      display: block;
      margin-bottom: 16px;
    }
  `;
nt([
  U({ attribute: !1 })
], gt.prototype, "hass", 2);
nt([
  E()
], gt.prototype, "_config", 2);
gt = nt([
  J("meraki-content-filter-card-editor")
], gt);
window.customCards = window.customCards || [];
window.customCards.some((e) => e.type === "meraki-content-filter-card") || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var kt = /* @__PURE__ */ ((e) => (e.GET_CONFIG = "meraki_ha/get_config", e.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", e.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", e.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", e.GET_VERSION = "meraki_ha/get_version", e.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", e.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", e.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", e.GET_GUEST_KEYS = "meraki_ha/ipsk/get", e.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", e.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", e))(kt || {});
const Gt = async (e, t) => {
  if (!e)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof e.callWS == "function")
      return await e.callWS(t);
    if (e.connection && typeof e.connection.sendMessagePromise == "function")
      return await e.connection.sendMessagePromise(t);
    throw new Error("Home Assistant WebSocket communication methods not found.");
  } catch (i) {
    throw console.error(`Meraki HA: WebSocket error [${t.type}]:`, i), i;
  }
};
var vt = {}, di = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, ke = {}, N = {};
let te;
const fi = [
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
  return fi[t];
};
N.getBCHDigit = function(e) {
  let t = 0;
  for (; e !== 0; )
    t++, e >>>= 1;
  return t;
};
N.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  te = t;
};
N.isKanjiModeEnabled = function() {
  return typeof te < "u";
};
N.toSJIS = function(t) {
  return te(t);
};
var It = {};
(function(e) {
  e.L = { bit: 1 }, e.M = { bit: 0 }, e.Q = { bit: 3 }, e.H = { bit: 2 };
  function t(i) {
    if (typeof i != "string")
      throw new Error("Param is not a string");
    switch (i.toLowerCase()) {
      case "l":
      case "low":
        return e.L;
      case "m":
      case "medium":
        return e.M;
      case "q":
      case "quartile":
        return e.Q;
      case "h":
      case "high":
        return e.H;
      default:
        throw new Error("Unknown EC Level: " + i);
    }
  }
  e.isValid = function(s) {
    return s && typeof s.bit < "u" && s.bit >= 0 && s.bit < 4;
  }, e.from = function(s, n) {
    if (e.isValid(s))
      return s;
    try {
      return t(s);
    } catch {
      return n;
    }
  };
})(It);
function Pe() {
  this.buffer = [], this.length = 0;
}
Pe.prototype = {
  get: function(e) {
    const t = Math.floor(e / 8);
    return (this.buffer[t] >>> 7 - e % 8 & 1) === 1;
  },
  put: function(e, t) {
    for (let i = 0; i < t; i++)
      this.putBit((e >>> t - i - 1 & 1) === 1);
  },
  getLengthInBits: function() {
    return this.length;
  },
  putBit: function(e) {
    const t = Math.floor(this.length / 8);
    this.buffer.length <= t && this.buffer.push(0), e && (this.buffer[t] |= 128 >>> this.length % 8), this.length++;
  }
};
var gi = Pe;
function Et(e) {
  if (!e || e < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = e, this.data = new Uint8Array(e * e), this.reservedBit = new Uint8Array(e * e);
}
Et.prototype.set = function(e, t, i, s) {
  const n = e * this.size + t;
  this.data[n] = i, s && (this.reservedBit[n] = !0);
};
Et.prototype.get = function(e, t) {
  return this.data[e * this.size + t];
};
Et.prototype.xor = function(e, t, i) {
  this.data[e * this.size + t] ^= i;
};
Et.prototype.isReserved = function(e, t) {
  return this.reservedBit[e * this.size + t];
};
var pi = Et, Ne = {};
(function(e) {
  const t = N.getSymbolSize;
  e.getRowColCoords = function(s) {
    if (s === 1) return [];
    const n = Math.floor(s / 7) + 2, r = t(s), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * n - 2)) * 2, c = [r - 7];
    for (let a = 1; a < n - 1; a++)
      c[a] = c[a - 1] - o;
    return c.push(6), c.reverse();
  }, e.getPositions = function(s) {
    const n = [], r = e.getRowColCoords(s), o = r.length;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        c === 0 && a === 0 || // top-left
        c === 0 && a === o - 1 || // bottom-left
        c === o - 1 && a === 0 || n.push([r[c], r[a]]);
    return n;
  };
})(Ne);
var Me = {};
const _i = N.getSymbolSize, ye = 7;
Me.getPositions = function(t) {
  const i = _i(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [i - ye, 0],
    // bottom-left
    [0, i - ye]
  ];
};
var Ie = {};
(function(e) {
  e.Patterns = {
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
  e.isValid = function(n) {
    return n != null && n !== "" && !isNaN(n) && n >= 0 && n <= 7;
  }, e.from = function(n) {
    return e.isValid(n) ? parseInt(n, 10) : void 0;
  }, e.getPenaltyN1 = function(n) {
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
  }, e.getPenaltyN2 = function(n) {
    const r = n.size;
    let o = 0;
    for (let c = 0; c < r - 1; c++)
      for (let a = 0; a < r - 1; a++) {
        const l = n.get(c, a) + n.get(c, a + 1) + n.get(c + 1, a) + n.get(c + 1, a + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, e.getPenaltyN3 = function(n) {
    const r = n.size;
    let o = 0, c = 0, a = 0;
    for (let l = 0; l < r; l++) {
      c = a = 0;
      for (let h = 0; h < r; h++)
        c = c << 1 & 2047 | n.get(l, h), h >= 10 && (c === 1488 || c === 93) && o++, a = a << 1 & 2047 | n.get(h, l), h >= 10 && (a === 1488 || a === 93) && o++;
    }
    return o * t.N3;
  }, e.getPenaltyN4 = function(n) {
    let r = 0;
    const o = n.data.length;
    for (let a = 0; a < o; a++) r += n.data[a];
    return Math.abs(Math.ceil(r * 100 / o / 5) - 10) * t.N4;
  };
  function i(s, n, r) {
    switch (s) {
      case e.Patterns.PATTERN000:
        return (n + r) % 2 === 0;
      case e.Patterns.PATTERN001:
        return n % 2 === 0;
      case e.Patterns.PATTERN010:
        return r % 3 === 0;
      case e.Patterns.PATTERN011:
        return (n + r) % 3 === 0;
      case e.Patterns.PATTERN100:
        return (Math.floor(n / 2) + Math.floor(r / 3)) % 2 === 0;
      case e.Patterns.PATTERN101:
        return n * r % 2 + n * r % 3 === 0;
      case e.Patterns.PATTERN110:
        return (n * r % 2 + n * r % 3) % 2 === 0;
      case e.Patterns.PATTERN111:
        return (n * r % 3 + (n + r) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + s);
    }
  }
  e.applyMask = function(n, r) {
    const o = r.size;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        r.isReserved(a, c) || r.xor(a, c, i(n, a, c));
  }, e.getBestMask = function(n, r) {
    const o = Object.keys(e.Patterns).length;
    let c = 0, a = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), e.applyMask(l, n);
      const h = e.getPenaltyN1(n) + e.getPenaltyN2(n) + e.getPenaltyN3(n) + e.getPenaltyN4(n);
      e.applyMask(l, n), h < a && (a = h, c = l);
    }
    return c;
  };
})(Ie);
var Tt = {};
const H = It, Ct = [
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
], bt = [
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
Tt.getBlocksCount = function(t, i) {
  switch (i) {
    case H.L:
      return Ct[(t - 1) * 4 + 0];
    case H.M:
      return Ct[(t - 1) * 4 + 1];
    case H.Q:
      return Ct[(t - 1) * 4 + 2];
    case H.H:
      return Ct[(t - 1) * 4 + 3];
    default:
      return;
  }
};
Tt.getTotalCodewordsCount = function(t, i) {
  switch (i) {
    case H.L:
      return bt[(t - 1) * 4 + 0];
    case H.M:
      return bt[(t - 1) * 4 + 1];
    case H.Q:
      return bt[(t - 1) * 4 + 2];
    case H.H:
      return bt[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var Te = {}, Bt = {};
const lt = new Uint8Array(512), Pt = new Uint8Array(256);
(function() {
  let t = 1;
  for (let i = 0; i < 255; i++)
    lt[i] = t, Pt[t] = i, t <<= 1, t & 256 && (t ^= 285);
  for (let i = 255; i < 512; i++)
    lt[i] = lt[i - 255];
})();
Bt.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return Pt[t];
};
Bt.exp = function(t) {
  return lt[t];
};
Bt.mul = function(t, i) {
  return t === 0 || i === 0 ? 0 : lt[Pt[t] + Pt[i]];
};
(function(e) {
  const t = Bt;
  e.mul = function(s, n) {
    const r = new Uint8Array(s.length + n.length - 1);
    for (let o = 0; o < s.length; o++)
      for (let c = 0; c < n.length; c++)
        r[o + c] ^= t.mul(s[o], n[c]);
    return r;
  }, e.mod = function(s, n) {
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
  }, e.generateECPolynomial = function(s) {
    let n = new Uint8Array([1]);
    for (let r = 0; r < s; r++)
      n = e.mul(n, new Uint8Array([1, t.exp(r)]));
    return n;
  };
})(Te);
const Be = Te;
function ee(e) {
  this.genPoly = void 0, this.degree = e, this.degree && this.initialize(this.degree);
}
ee.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = Be.generateECPolynomial(this.degree);
};
ee.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const i = new Uint8Array(t.length + this.degree);
  i.set(t);
  const s = Be.mod(i, this.genPoly), n = this.degree - s.length;
  if (n > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(s, n), r;
  }
  return s;
};
var mi = ee, xe = {}, z = {}, ie = {};
ie.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var x = {};
const De = "[0-9]+", yi = "[A-Z $%*+\\-./:]+";
let pt = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
pt = pt.replace(/u/g, "\\u");
const wi = "(?:(?![A-Z0-9 $%*+\\-./:]|" + pt + `)(?:.|[\r
]))+`;
x.KANJI = new RegExp(pt, "g");
x.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
x.BYTE = new RegExp(wi, "g");
x.NUMERIC = new RegExp(De, "g");
x.ALPHANUMERIC = new RegExp(yi, "g");
const vi = new RegExp("^" + pt + "$"), Ei = new RegExp("^" + De + "$"), Ci = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
x.testKanji = function(t) {
  return vi.test(t);
};
x.testNumeric = function(t) {
  return Ei.test(t);
};
x.testAlphanumeric = function(t) {
  return Ci.test(t);
};
(function(e) {
  const t = ie, i = x;
  e.NUMERIC = {
    id: "Numeric",
    bit: 1,
    ccBits: [10, 12, 14]
  }, e.ALPHANUMERIC = {
    id: "Alphanumeric",
    bit: 2,
    ccBits: [9, 11, 13]
  }, e.BYTE = {
    id: "Byte",
    bit: 4,
    ccBits: [8, 16, 16]
  }, e.KANJI = {
    id: "Kanji",
    bit: 8,
    ccBits: [8, 10, 12]
  }, e.MIXED = {
    bit: -1
  }, e.getCharCountIndicator = function(r, o) {
    if (!r.ccBits) throw new Error("Invalid mode: " + r);
    if (!t.isValid(o))
      throw new Error("Invalid version: " + o);
    return o >= 1 && o < 10 ? r.ccBits[0] : o < 27 ? r.ccBits[1] : r.ccBits[2];
  }, e.getBestModeForData = function(r) {
    return i.testNumeric(r) ? e.NUMERIC : i.testAlphanumeric(r) ? e.ALPHANUMERIC : i.testKanji(r) ? e.KANJI : e.BYTE;
  }, e.toString = function(r) {
    if (r && r.id) return r.id;
    throw new Error("Invalid mode");
  }, e.isValid = function(r) {
    return r && r.bit && r.ccBits;
  };
  function s(n) {
    if (typeof n != "string")
      throw new Error("Param is not a string");
    switch (n.toLowerCase()) {
      case "numeric":
        return e.NUMERIC;
      case "alphanumeric":
        return e.ALPHANUMERIC;
      case "kanji":
        return e.KANJI;
      case "byte":
        return e.BYTE;
      default:
        throw new Error("Unknown mode: " + n);
    }
  }
  e.from = function(r, o) {
    if (e.isValid(r))
      return r;
    try {
      return s(r);
    } catch {
      return o;
    }
  };
})(z);
(function(e) {
  const t = N, i = Tt, s = It, n = z, r = ie, o = 7973, c = t.getBCHDigit(o);
  function a(d, u, _) {
    for (let y = 1; y <= 40; y++)
      if (u <= e.getCapacity(y, _, d))
        return y;
  }
  function l(d, u) {
    return n.getCharCountIndicator(d, u) + 4;
  }
  function h(d, u) {
    let _ = 0;
    return d.forEach(function(y) {
      const k = l(y.mode, u);
      _ += k + y.getBitsLength();
    }), _;
  }
  function f(d, u) {
    for (let _ = 1; _ <= 40; _++)
      if (h(d, _) <= e.getCapacity(_, u, n.MIXED))
        return _;
  }
  e.from = function(u, _) {
    return r.isValid(u) ? parseInt(u, 10) : _;
  }, e.getCapacity = function(u, _, y) {
    if (!r.isValid(u))
      throw new Error("Invalid QR Code version");
    typeof y > "u" && (y = n.BYTE);
    const k = t.getSymbolTotalCodewords(u), m = i.getTotalCodewordsCount(u, _), w = (k - m) * 8;
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
  }, e.getBestVersionForData = function(u, _) {
    let y;
    const k = s.from(_, s.M);
    if (Array.isArray(u)) {
      if (u.length > 1)
        return f(u, k);
      if (u.length === 0)
        return 1;
      y = u[0];
    } else
      y = u;
    return a(y.mode, y.getLength(), k);
  }, e.getEncodedBits = function(u) {
    if (!r.isValid(u) || u < 7)
      throw new Error("Invalid QR Code version");
    let _ = u << 12;
    for (; t.getBCHDigit(_) - c >= 0; )
      _ ^= o << t.getBCHDigit(_) - c;
    return u << 12 | _;
  };
})(xe);
var Re = {};
const Kt = N, Ue = 1335, bi = 21522, we = Kt.getBCHDigit(Ue);
Re.getEncodedBits = function(t, i) {
  const s = t.bit << 3 | i;
  let n = s << 10;
  for (; Kt.getBCHDigit(n) - we >= 0; )
    n ^= Ue << Kt.getBCHDigit(n) - we;
  return (s << 10 | n) ^ bi;
};
var Le = {};
const $i = z;
function X(e) {
  this.mode = $i.NUMERIC, this.data = e.toString();
}
X.getBitsLength = function(t) {
  return 10 * Math.floor(t / 3) + (t % 3 ? t % 3 * 3 + 1 : 0);
};
X.prototype.getLength = function() {
  return this.data.length;
};
X.prototype.getBitsLength = function() {
  return X.getBitsLength(this.data.length);
};
X.prototype.write = function(t) {
  let i, s, n;
  for (i = 0; i + 3 <= this.data.length; i += 3)
    s = this.data.substr(i, 3), n = parseInt(s, 10), t.put(n, 10);
  const r = this.data.length - i;
  r > 0 && (s = this.data.substr(i), n = parseInt(s, 10), t.put(n, r * 3 + 1));
};
var Si = X;
const Ai = z, Ht = [
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
function tt(e) {
  this.mode = Ai.ALPHANUMERIC, this.data = e;
}
tt.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
tt.prototype.getLength = function() {
  return this.data.length;
};
tt.prototype.getBitsLength = function() {
  return tt.getBitsLength(this.data.length);
};
tt.prototype.write = function(t) {
  let i;
  for (i = 0; i + 2 <= this.data.length; i += 2) {
    let s = Ht.indexOf(this.data[i]) * 45;
    s += Ht.indexOf(this.data[i + 1]), t.put(s, 11);
  }
  this.data.length % 2 && t.put(Ht.indexOf(this.data[i]), 6);
};
var ki = tt;
const Pi = z;
function et(e) {
  this.mode = Pi.BYTE, typeof e == "string" ? this.data = new TextEncoder().encode(e) : this.data = new Uint8Array(e);
}
et.getBitsLength = function(t) {
  return t * 8;
};
et.prototype.getLength = function() {
  return this.data.length;
};
et.prototype.getBitsLength = function() {
  return et.getBitsLength(this.data.length);
};
et.prototype.write = function(e) {
  for (let t = 0, i = this.data.length; t < i; t++)
    e.put(this.data[t], 8);
};
var Ni = et;
const Mi = z, Ii = N;
function it(e) {
  this.mode = Mi.KANJI, this.data = e;
}
it.getBitsLength = function(t) {
  return t * 13;
};
it.prototype.getLength = function() {
  return this.data.length;
};
it.prototype.getBitsLength = function() {
  return it.getBitsLength(this.data.length);
};
it.prototype.write = function(e) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let i = Ii.toSJIS(this.data[t]);
    if (i >= 33088 && i <= 40956)
      i -= 33088;
    else if (i >= 57408 && i <= 60351)
      i -= 49472;
    else
      throw new Error(
        "Invalid SJIS character: " + this.data[t] + `
Make sure your charset is UTF-8`
      );
    i = (i >>> 8 & 255) * 192 + (i & 255), e.put(i, 13);
  }
};
var Ti = it, Oe = { exports: {} };
(function(e) {
  var t = {
    single_source_shortest_paths: function(i, s, n) {
      var r = {}, o = {};
      o[s] = 0;
      var c = t.PriorityQueue.make();
      c.push(s, 0);
      for (var a, l, h, f, d, u, _, y, k; !c.empty(); ) {
        a = c.pop(), l = a.value, f = a.cost, d = i[l] || {};
        for (h in d)
          d.hasOwnProperty(h) && (u = d[h], _ = f + u, y = o[h], k = typeof o[h] > "u", (k || y > _) && (o[h] = _, c.push(h, _), r[h] = l));
      }
      if (typeof n < "u" && typeof o[n] > "u") {
        var m = ["Could not find a path from ", s, " to ", n, "."].join("");
        throw new Error(m);
      }
      return r;
    },
    extract_shortest_path_from_predecessor_list: function(i, s) {
      for (var n = [], r = s; r; )
        n.push(r), i[r], r = i[r];
      return n.reverse(), n;
    },
    find_path: function(i, s, n) {
      var r = t.single_source_shortest_paths(i, s, n);
      return t.extract_shortest_path_from_predecessor_list(
        r,
        n
      );
    },
    /**
     * A very naive priority queue implementation.
     */
    PriorityQueue: {
      make: function(i) {
        var s = t.PriorityQueue, n = {}, r;
        i = i || {};
        for (r in s)
          s.hasOwnProperty(r) && (n[r] = s[r]);
        return n.queue = [], n.sorter = i.sorter || s.default_sorter, n;
      },
      default_sorter: function(i, s) {
        return i.cost - s.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(i, s) {
        var n = { value: i, cost: s };
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
  e.exports = t;
})(Oe);
var Bi = Oe.exports;
(function(e) {
  const t = z, i = Si, s = ki, n = Ni, r = Ti, o = x, c = N, a = Bi;
  function l(m) {
    return unescape(encodeURIComponent(m)).length;
  }
  function h(m, w, p) {
    const g = [];
    let C;
    for (; (C = m.exec(p)) !== null; )
      g.push({
        data: C[0],
        index: C.index,
        mode: w,
        length: C[0].length
      });
    return g;
  }
  function f(m) {
    const w = h(o.NUMERIC, t.NUMERIC, m), p = h(o.ALPHANUMERIC, t.ALPHANUMERIC, m);
    let g, C;
    return c.isKanjiModeEnabled() ? (g = h(o.BYTE, t.BYTE, m), C = h(o.KANJI, t.KANJI, m)) : (g = h(o.BYTE_KANJI, t.BYTE, m), C = []), w.concat(p, g, C).sort(function(S, I) {
      return S.index - I.index;
    }).map(function(S) {
      return {
        data: S.data,
        mode: S.mode,
        length: S.length
      };
    });
  }
  function d(m, w) {
    switch (w) {
      case t.NUMERIC:
        return i.getBitsLength(m);
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
    let C = ["start"];
    for (let b = 0; b < m.length; b++) {
      const S = m[b], I = [];
      for (let L = 0; L < S.length; L++) {
        const B = S[L], rt = "" + b + L;
        I.push(rt), p[rt] = { node: B, lastCount: 0 }, g[rt] = {};
        for (let Dt = 0; Dt < C.length; Dt++) {
          const D = C[Dt];
          p[D] && p[D].node.mode === B.mode ? (g[D][rt] = d(p[D].lastCount + B.length, B.mode) - d(p[D].lastCount, B.mode), p[D].lastCount += B.length) : (p[D] && (p[D].lastCount = B.length), g[D][rt] = d(B.length, B.mode) + 4 + t.getCharCountIndicator(B.mode, w));
        }
      }
      C = I;
    }
    for (let b = 0; b < C.length; b++)
      g[C[b]].end = 0;
    return { map: g, table: p };
  }
  function k(m, w) {
    let p;
    const g = t.getBestModeForData(m);
    if (p = t.from(w, g), p !== t.BYTE && p.bit < g.bit)
      throw new Error('"' + m + '" cannot be encoded with mode ' + t.toString(p) + `.
 Suggested mode is: ` + t.toString(g));
    switch (p === t.KANJI && !c.isKanjiModeEnabled() && (p = t.BYTE), p) {
      case t.NUMERIC:
        return new i(m);
      case t.ALPHANUMERIC:
        return new s(m);
      case t.KANJI:
        return new r(m);
      case t.BYTE:
        return new n(m);
    }
  }
  e.fromArray = function(w) {
    return w.reduce(function(p, g) {
      return typeof g == "string" ? p.push(k(g, null)) : g.data && p.push(k(g.data, g.mode)), p;
    }, []);
  }, e.fromString = function(w, p) {
    const g = f(w, c.isKanjiModeEnabled()), C = _(g), b = y(C, p), S = a.find_path(b.map, "start", "end"), I = [];
    for (let L = 1; L < S.length - 1; L++)
      I.push(b.table[S[L]].node);
    return e.fromArray(u(I));
  }, e.rawSplit = function(w) {
    return e.fromArray(
      f(w, c.isKanjiModeEnabled())
    );
  };
})(Le);
const xt = N, Vt = It, xi = gi, Di = pi, Ri = Ne, Ui = Me, qt = Ie, Wt = Tt, Li = mi, Nt = xe, Oi = Re, Hi = z, Ft = Le;
function Vi(e, t) {
  const i = e.size, s = Ui.getPositions(t);
  for (let n = 0; n < s.length; n++) {
    const r = s[n][0], o = s[n][1];
    for (let c = -1; c <= 7; c++)
      if (!(r + c <= -1 || i <= r + c))
        for (let a = -1; a <= 7; a++)
          o + a <= -1 || i <= o + a || (c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 2 && c <= 4 && a >= 2 && a <= 4 ? e.set(r + c, o + a, !0, !0) : e.set(r + c, o + a, !1, !0));
  }
}
function Fi(e) {
  const t = e.size;
  for (let i = 8; i < t - 8; i++) {
    const s = i % 2 === 0;
    e.set(i, 6, s, !0), e.set(6, i, s, !0);
  }
}
function zi(e, t) {
  const i = Ri.getPositions(t);
  for (let s = 0; s < i.length; s++) {
    const n = i[s][0], r = i[s][1];
    for (let o = -2; o <= 2; o++)
      for (let c = -2; c <= 2; c++)
        o === -2 || o === 2 || c === -2 || c === 2 || o === 0 && c === 0 ? e.set(n + o, r + c, !0, !0) : e.set(n + o, r + c, !1, !0);
  }
}
function ji(e, t) {
  const i = e.size, s = Nt.getEncodedBits(t);
  let n, r, o;
  for (let c = 0; c < 18; c++)
    n = Math.floor(c / 3), r = c % 3 + i - 8 - 3, o = (s >> c & 1) === 1, e.set(n, r, o, !0), e.set(r, n, o, !0);
}
function zt(e, t, i) {
  const s = e.size, n = Oi.getEncodedBits(t, i);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (n >> r & 1) === 1, r < 6 ? e.set(r, 8, o, !0) : r < 8 ? e.set(r + 1, 8, o, !0) : e.set(s - 15 + r, 8, o, !0), r < 8 ? e.set(8, s - r - 1, o, !0) : r < 9 ? e.set(8, 15 - r - 1 + 1, o, !0) : e.set(8, 15 - r - 1, o, !0);
  e.set(s - 8, 8, 1, !0);
}
function Gi(e, t) {
  const i = e.size;
  let s = -1, n = i - 1, r = 7, o = 0;
  for (let c = i - 1; c > 0; c -= 2)
    for (c === 6 && c--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!e.isReserved(n, c - a)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), e.set(n, c - a, l), r--, r === -1 && (o++, r = 7);
        }
      if (n += s, n < 0 || i <= n) {
        n -= s, s = -s;
        break;
      }
    }
}
function Ki(e, t, i) {
  const s = new xi();
  i.forEach(function(a) {
    s.put(a.mode.bit, 4), s.put(a.getLength(), Hi.getCharCountIndicator(a.mode, e)), a.write(s);
  });
  const n = xt.getSymbolTotalCodewords(e), r = Wt.getTotalCodewordsCount(e, t), o = (n - r) * 8;
  for (s.getLengthInBits() + 4 <= o && s.put(0, 4); s.getLengthInBits() % 8 !== 0; )
    s.putBit(0);
  const c = (o - s.getLengthInBits()) / 8;
  for (let a = 0; a < c; a++)
    s.put(a % 2 ? 17 : 236, 8);
  return qi(s, e, t);
}
function qi(e, t, i) {
  const s = xt.getSymbolTotalCodewords(t), n = Wt.getTotalCodewordsCount(t, i), r = s - n, o = Wt.getBlocksCount(t, i), c = s % o, a = o - c, l = Math.floor(s / o), h = Math.floor(r / o), f = h + 1, d = l - h, u = new Li(d);
  let _ = 0;
  const y = new Array(o), k = new Array(o);
  let m = 0;
  const w = new Uint8Array(e.buffer);
  for (let S = 0; S < o; S++) {
    const I = S < a ? h : f;
    y[S] = w.slice(_, _ + I), k[S] = u.encode(y[S]), _ += I, m = Math.max(m, I);
  }
  const p = new Uint8Array(s);
  let g = 0, C, b;
  for (C = 0; C < m; C++)
    for (b = 0; b < o; b++)
      C < y[b].length && (p[g++] = y[b][C]);
  for (C = 0; C < d; C++)
    for (b = 0; b < o; b++)
      p[g++] = k[b][C];
  return p;
}
function Wi(e, t, i, s) {
  let n;
  if (Array.isArray(e))
    n = Ft.fromArray(e);
  else if (typeof e == "string") {
    let l = t;
    if (!l) {
      const h = Ft.rawSplit(e);
      l = Nt.getBestVersionForData(h, i);
    }
    n = Ft.fromString(e, l || 40);
  } else
    throw new Error("Invalid data");
  const r = Nt.getBestVersionForData(n, i);
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
  const o = Ki(t, i, n), c = xt.getSymbolSize(t), a = new Di(c);
  return Vi(a, t), Fi(a), zi(a, t), zt(a, i, 0), t >= 7 && ji(a, t), Gi(a, o), isNaN(s) && (s = qt.getBestMask(
    a,
    zt.bind(null, a, i)
  )), qt.applyMask(s, a), zt(a, i, s), {
    modules: a,
    version: t,
    errorCorrectionLevel: i,
    maskPattern: s,
    segments: n
  };
}
ke.create = function(t, i) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let s = Vt.M, n, r;
  return typeof i < "u" && (s = Vt.from(i.errorCorrectionLevel, Vt.M), n = Nt.from(i.version), r = qt.from(i.maskPattern), i.toSJISFunc && xt.setToSJISFunction(i.toSJISFunc)), Wi(t, n, s, r);
};
var He = {}, ne = {};
(function(e) {
  function t(i) {
    if (typeof i == "number" && (i = i.toString()), typeof i != "string")
      throw new Error("Color should be defined as hex string");
    let s = i.slice().replace("#", "").split("");
    if (s.length < 3 || s.length === 5 || s.length > 8)
      throw new Error("Invalid hex color: " + i);
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
  e.getOptions = function(s) {
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
  }, e.getScale = function(s, n) {
    return n.width && n.width >= s + n.margin * 2 ? n.width / (s + n.margin * 2) : n.scale;
  }, e.getImageWidth = function(s, n) {
    const r = e.getScale(s, n);
    return Math.floor((s + n.margin * 2) * r);
  }, e.qrToImageData = function(s, n, r) {
    const o = n.modules.size, c = n.modules.data, a = e.getScale(o, r), l = Math.floor((o + r.margin * 2) * a), h = r.margin * a, f = [r.color.light, r.color.dark];
    for (let d = 0; d < l; d++)
      for (let u = 0; u < l; u++) {
        let _ = (d * l + u) * 4, y = r.color.light;
        if (d >= h && u >= h && d < l - h && u < l - h) {
          const k = Math.floor((d - h) / a), m = Math.floor((u - h) / a);
          y = f[c[k * o + m] ? 1 : 0];
        }
        s[_++] = y.r, s[_++] = y.g, s[_++] = y.b, s[_] = y.a;
      }
  };
})(ne);
(function(e) {
  const t = ne;
  function i(n, r, o) {
    n.clearRect(0, 0, r.width, r.height), r.style || (r.style = {}), r.height = o, r.width = o, r.style.height = o + "px", r.style.width = o + "px";
  }
  function s() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  e.render = function(r, o, c) {
    let a = c, l = o;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), o || (l = s()), a = t.getOptions(a);
    const h = t.getImageWidth(r.modules.size, a), f = l.getContext("2d"), d = f.createImageData(h, h);
    return t.qrToImageData(d.data, r, a), i(f, l, h), f.putImageData(d, 0, 0), l;
  }, e.renderToDataURL = function(r, o, c) {
    let a = c;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), a || (a = {});
    const l = e.render(r, o, a), h = a.type || "image/png", f = a.rendererOpts || {};
    return l.toDataURL(h, f.quality);
  };
})(He);
var Ve = {};
const Ji = ne;
function ve(e, t) {
  const i = e.a / 255, s = t + '="' + e.hex + '"';
  return i < 1 ? s + " " + t + '-opacity="' + i.toFixed(2).slice(1) + '"' : s;
}
function jt(e, t, i) {
  let s = e + t;
  return typeof i < "u" && (s += " " + i), s;
}
function Yi(e, t, i) {
  let s = "", n = 0, r = !1, o = 0;
  for (let c = 0; c < e.length; c++) {
    const a = Math.floor(c % t), l = Math.floor(c / t);
    !a && !r && (r = !0), e[c] ? (o++, c > 0 && a > 0 && e[c - 1] || (s += r ? jt("M", a + i, 0.5 + l + i) : jt("m", n, 0), n = 0, r = !1), a + 1 < t && e[c + 1] || (s += jt("h", o), o = 0)) : n++;
  }
  return s;
}
Ve.render = function(t, i, s) {
  const n = Ji.getOptions(i), r = t.modules.size, o = t.modules.data, c = r + n.margin * 2, a = n.color.light.a ? "<path " + ve(n.color.light, "fill") + ' d="M0 0h' + c + "v" + c + 'H0z"/>' : "", l = "<path " + ve(n.color.dark, "stroke") + ' d="' + Yi(o, r, n.margin) + '"/>', h = 'viewBox="0 0 ' + c + " " + c + '"', d = '<svg xmlns="http://www.w3.org/2000/svg" ' + (n.width ? 'width="' + n.width + '" height="' + n.width + '" ' : "") + h + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof s == "function" && s(null, d), d;
};
const Qi = di, Jt = ke, Fe = He, Zi = Ve;
function se(e, t, i, s, n) {
  const r = [].slice.call(arguments, 1), o = r.length, c = typeof r[o - 1] == "function";
  if (!c && !Qi())
    throw new Error("Callback required as last argument");
  if (c) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (n = i, i = t, t = s = void 0) : o === 3 && (t.getContext && typeof n > "u" ? (n = s, s = void 0) : (n = s, s = i, i = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (i = t, t = s = void 0) : o === 2 && !t.getContext && (s = i, i = t, t = void 0), new Promise(function(a, l) {
      try {
        const h = Jt.create(i, s);
        a(e(h, t, s));
      } catch (h) {
        l(h);
      }
    });
  }
  try {
    const a = Jt.create(i, s);
    n(null, e(a, t, s));
  } catch (a) {
    n(a);
  }
}
vt.create = Jt.create;
vt.toCanvas = se.bind(null, Fe.render);
vt.toDataURL = se.bind(null, Fe.renderToDataURL);
vt.toString = se.bind(null, function(e, t, i) {
  return Zi.render(e, i);
});
var Xi = Object.defineProperty, tn = Object.getOwnPropertyDescriptor, T = (e, t, i, s) => {
  for (var n = s > 1 ? void 0 : s ? tn(t, i) : t, r = e.length - 1, o; r >= 0; r--)
    (o = e[r]) && (n = (s ? o(t, i, n) : o(n)) || n);
  return s && n && Xi(t, i, n), n;
};
let R = class extends M {
  constructor() {
    super(...arguments), this._networks = [], this._ssids = [], this._selectedNetwork = "", this._loading = !1;
  }
  setConfig(e) {
    this._config = e;
  }
  firstUpdated(e) {
    super.firstUpdated(e), this._fetchInitialData();
  }
  async _fetchInitialData() {
    if (this.hass) {
      this._loading = !0;
      try {
        const e = await this.hass.callWS({
          type: "config_entries/get",
          domain: "meraki_ha"
        }), t = e.length > 0 ? e[0].entry_id : null;
        if (!t) return;
        const i = await Gt(this.hass, {
          type: kt.GET_CONFIG,
          config_entry_id: t
        });
        this._networks = (Array.isArray(i.networks) ? i.networks : []).filter((s) => {
          var n;
          return (n = s.productTypes) == null ? void 0 : n.includes("wireless");
        }), this._ssids = Array.isArray(i.ssids) ? i.ssids : [];
      } catch (e) {
        console.error("Failed to fetch Meraki data:", e);
      } finally {
        this._loading = !1;
      }
    }
  }
  _handleNetworkChange(e) {
    e.stopPropagation(), this._selectedNetwork = e.target.value;
  }
  _handleSSIDSelect(e) {
    e.stopPropagation();
    const t = e.target.value, i = this._ssids.find((s) => s.networkId === this._selectedNetwork && String(s.number) === t);
    if (i && this._config) {
      const s = {
        ...this._config,
        ssid: i.name,
        password: i.psk || ""
      };
      this._config = s, this._dispatchEvent(s);
    }
  }
  _valueChanged(e) {
    if (!this._config) return;
    const t = e.target, i = t.configValue;
    if (this._config[i] === t.value) return;
    const s = {
      ...this._config,
      [i]: t.value
    };
    this._config = s, this._dispatchEvent(s);
  }
  _dispatchEvent(e) {
    const t = new CustomEvent("config-changed", {
      detail: { config: e },
      bubbles: !0,
      composed: !0
    });
    this.dispatchEvent(t);
  }
  render() {
    if (!this.hass || !this._config) return v``;
    const e = this._ssids.filter((t) => t.networkId === this._selectedNetwork);
    return v`
      <div class="card-config">
        <ha-select
          label="Network (Optional - to populate SSID)"
          .value=${this._selectedNetwork}
          @closed=${this._handleNetworkChange}
          fixedMenuPosition
          naturalMenuWidth
        >
          <mwc-list-item value="">Select a network</mwc-list-item>
          ${this._networks.map((t) => v`<mwc-list-item value="${t.id}">${t.name}</mwc-list-item>`)}
        </ha-select>

        <ha-select
          label="SSID from Meraki"
          .value=${""}
          .disabled=${!this._selectedNetwork}
          @closed=${this._handleSSIDSelect}
          fixedMenuPosition
          naturalMenuWidth
        >
          <mwc-list-item value="">Select an SSID</mwc-list-item>
          ${e.map((t) => v`<mwc-list-item value="${String(t.number)}">${t.name}</mwc-list-item>`)}
        </ha-select>

        <ha-textfield
          label="SSID Name or Entity ID"
          .value=${this._config.ssid || ""}
          .configValue=${"ssid"}
          @input=${this._valueChanged}
        ></ha-textfield>

        <ha-textfield
          label="Password or Entity ID"
          .value=${this._config.password || ""}
          .configValue=${"password"}
          @input=${this._valueChanged}
        ></ha-textfield>

        <ha-textfield
          label="Card Title"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }
};
R.styles = F`
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
T([
  U({ attribute: !1 })
], R.prototype, "hass", 2);
T([
  E()
], R.prototype, "_config", 2);
T([
  E()
], R.prototype, "_networks", 2);
T([
  E()
], R.prototype, "_ssids", 2);
T([
  E()
], R.prototype, "_selectedNetwork", 2);
T([
  E()
], R.prototype, "_loading", 2);
R = T([
  J("meraki-wifi-qr-card-editor")
], R);
let W = class extends M {
  constructor() {
    super(...arguments), this._qrSvg = "";
  }
  static async getConfigElement() {
    return document.createElement("meraki-wifi-qr-card-editor");
  }
  setConfig(e) {
    if (!e || !e.ssid)
      throw new Error("Please define an SSID");
    this._config = e;
  }
  static getStubConfig() {
    return {
      ssid: "Guest WiFi",
      password: "password123",
      name: "Wi-Fi Access"
    };
  }
  updated(e) {
    var t, i, s, n;
    if (e.has("hass") || e.has("_config")) {
      const r = e.has("hass") ? this._getValueFromHass((t = this._config) == null ? void 0 : t.ssid, e.get("hass")) : null, o = this._getValue((i = this._config) == null ? void 0 : i.ssid), c = e.has("hass") ? this._getValueFromHass((s = this._config) == null ? void 0 : s.password, e.get("hass")) : null, a = this._getValue((n = this._config) == null ? void 0 : n.password);
      (e.has("_config") || r !== o || c !== a) && this._generateQR();
    }
  }
  _getValueFromHass(e, t) {
    return !e || !t ? e || "" : t.states[e] ? t.states[e].state : e;
  }
  _getValue(e) {
    return !e || !this.hass ? e || "" : this.hass.states[e] ? this.hass.states[e].state : e;
  }
  _generateWifiString(e, t) {
    const i = e.replace(/([\\;,":])/g, "\\$1"), s = t ? t.replace(/([\\;,":])/g, "\\$1") : "";
    return s ? `WIFI:T:WPA;S:${i};P:${s};;` : `WIFI:T:nopass;S:${i};P:;;`;
  }
  async _generateQR() {
    if (!this._config) return;
    const e = this._getValue(this._config.ssid), t = this._getValue(this._config.password);
    if (!e) {
      this._qrSvg = "";
      return;
    }
    const i = this._generateWifiString(e, t);
    try {
      this._qrSvg = await vt.toString(i, {
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
      return v``;
    const e = this._getValue(this._config.ssid), t = this._getValue(this._config.password);
    return v`
      <ha-card .header="${this._config.name || "Wi-Fi Access"}">
        <div class="card-content">
          <div class="ssid-display">${e}</div>
          <div class="qr-container" .innerHTML="${this._qrSvg}"></div>
          ${t ? v`<div class="password-display">Password: <code>${t}</code></div>` : ""}
        </div>
      </ha-card>
    `;
  }
};
W.styles = F`
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
T([
  U({ attribute: !1 })
], W.prototype, "hass", 2);
T([
  E()
], W.prototype, "_config", 2);
T([
  E()
], W.prototype, "_qrSvg", 2);
W = T([
  J("meraki-wifi-qr-card")
], W);
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", W);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var en = Object.defineProperty, nn = Object.getOwnPropertyDescriptor, st = (e, t, i, s) => {
  for (var n = s > 1 ? void 0 : s ? nn(t, i) : t, r = e.length - 1, o; r >= 0; r--)
    (o = e[r]) && (n = (s ? o(t, i, n) : o(n)) || n);
  return s && n && en(t, i, n), n;
};
let _t = class extends M {
  static async getConfigElement() {
    return document.createElement("meraki-network-vitals-card-editor");
  }
  setConfig(e) {
    if (!e)
      throw new Error("Invalid configuration");
    this._config = e;
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
  _renderStatusDot(e, t) {
    if (!e || !this.hass.states[e])
      return v`
        <div class="status-item">
          <svg height="12" width="12">
            <circle cx="6" cy="6" r="6" fill="var(--disabled-text-color)" />
          </svg>
          <span class="status-label">${t}</span>
        </div>
      `;
    const i = this.hass.states[e], s = i ? i.state.toLowerCase() : "unknown";
    let n = "var(--disabled-text-color)";
    return s === "ok" || s === "online" || s === "connected" ? n = "var(--success-color)" : s === "warning" ? n = "var(--warning-color)" : (s === "error" || s === "offline" || s === "failed") && (n = "var(--error-color)"), v`
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
      return v``;
    const e = this._config.throughput_entity, t = e && this.hass.states[e] ? this.hass.states[e].state + " " + (this.hass.states[e].attributes.unit_of_measurement || "") : "N/A";
    return v`
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
_t.styles = F`
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
st([
  U({ attribute: !1 })
], _t.prototype, "hass", 2);
st([
  E()
], _t.prototype, "_config", 2);
_t = st([
  J("meraki-network-vitals-card")
], _t);
let mt = class extends M {
  setConfig(e) {
    this._config = e;
  }
  render() {
    return !this.hass || !this._config ? v`` : v`
      <div class="card-config">
        <ha-textfield
          label="Name (Optional)"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
          style="width: 100%; margin-bottom: 16px;"
        ></ha-textfield>
        <ha-entity-picker
          label="Gateway Entity"
          .hass=${this.hass}
          .value=${this._config.gateway_entity || ""}
          .configValue=${"gateway_entity"}
          @value-changed=${this._valueChanged}
          allow-custom-entity
          style="width: 100%; margin-bottom: 16px; display: block;"
        ></ha-entity-picker>
        <ha-entity-picker
          label="Switch Entity"
          .hass=${this.hass}
          .value=${this._config.switch_entity || ""}
          .configValue=${"switch_entity"}
          @value-changed=${this._valueChanged}
          allow-custom-entity
          style="width: 100%; margin-bottom: 16px; display: block;"
        ></ha-entity-picker>
        <ha-entity-picker
          label="AP Entity"
          .hass=${this.hass}
          .value=${this._config.ap_entity || ""}
          .configValue=${"ap_entity"}
          @value-changed=${this._valueChanged}
          allow-custom-entity
          style="width: 100%; margin-bottom: 16px; display: block;"
        ></ha-entity-picker>
        <ha-entity-picker
          label="Throughput Entity"
          .hass=${this.hass}
          .value=${this._config.throughput_entity || ""}
          .configValue=${"throughput_entity"}
          @value-changed=${this._valueChanged}
          allow-custom-entity
          style="width: 100%; display: block;"
        ></ha-entity-picker>
      </div>
    `;
  }
  _valueChanged(e) {
    if (!this._config || !this.hass) return;
    const t = e.target, i = t.value, s = t.configValue;
    if (this._config[s] === i) return;
    const n = {
      ...this._config,
      [s]: i
    }, r = new CustomEvent("config-changed", {
      detail: { config: n },
      bubbles: !0,
      composed: !0
    });
    this.dispatchEvent(r);
  }
};
mt.styles = F`
    .card-config {
      display: flex;
      flex-direction: column;
    }
  `;
st([
  U({ attribute: !1 })
], mt.prototype, "hass", 2);
st([
  E()
], mt.prototype, "_config", 2);
mt = st([
  J("meraki-network-vitals-card-editor")
], mt);
window.customCards = window.customCards || [];
window.customCards.some((e) => e.type === "meraki-network-vitals-card") || window.customCards.push({
  type: "meraki-network-vitals-card",
  name: "Meraki Network Vitals",
  description: "Compact horizontal header for Meraki network health and throughput.",
  preview: !0
});
var sn = Object.defineProperty, rn = Object.getOwnPropertyDescriptor, re = (e, t, i, s) => {
  for (var n = s > 1 ? void 0 : s ? rn(t, i) : t, r = e.length - 1, o; r >= 0; r--)
    (o = e[r]) && (n = (s ? o(t, i, n) : o(n)) || n);
  return s && n && sn(t, i, n), n;
};
let yt = class extends M {
  setConfig(e) {
    this._config = e;
  }
  render() {
    return !this.hass || !this._config ? v`` : v`
      <div class="card-config">
        <ha-textfield
          label="Name (Optional)"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
          style="width: 100%; margin-bottom: 16px;"
        ></ha-textfield>
      </div>
    `;
  }
  _valueChanged(e) {
    if (!this._config || !this.hass) return;
    const t = e.target, i = t.value, s = t.configValue;
    if (this._config[s] === i) return;
    const n = {
      ...this._config,
      [s]: i
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
yt.styles = F`
    .card-config {
      display: flex;
      flex-direction: column;
    }
  `;
re([
  U({ attribute: !1 })
], yt.prototype, "hass", 2);
re([
  E()
], yt.prototype, "_config", 2);
yt = re([
  J("meraki-guest-access-card-editor")
], yt);
var on = Object.defineProperty, P = (e, t, i, s) => {
  for (var n = void 0, r = e.length - 1, o; r >= 0; r--)
    (o = e[r]) && (n = o(t, i, n) || n);
  return n && on(t, i, n), n;
};
const oe = class oe extends M {
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
    var i;
    super.updated(t), t.has("hass") && this.hass && (!this._initDone && this.hass && this._fetchInitialData(), (i = this.hass.user) != null && i.name && !this._customName && (this._customName = this.hass.user.name));
  }
  async _fetchInitialData() {
    var t;
    if (this._initDone = !0, !!this.hass) {
      this._loading = !0;
      try {
        const i = await this.hass.callWS({
          type: "config_entries/get",
          domain: "meraki_ha"
        }), s = ((t = this._config) == null ? void 0 : t.config_entry_id) || (i.length > 0 ? i[0].entry_id : null);
        if (!s) {
          this._error = "Meraki integration not found. Please configure it first.", this._loading = !1;
          return;
        }
        const n = await Gt(this.hass, {
          type: kt.GET_CONFIG,
          config_entry_id: s
        });
        this._networks = (Array.isArray(n.networks) ? n.networks : []).filter((r) => {
          var o;
          return (o = r.productTypes) == null ? void 0 : o.includes("wireless");
        }), this._ssids = Array.isArray(n.ssids) ? n.ssids : [], this._networks.length > 0 && !this._selectedNetwork && (this._selectedNetwork = this._networks[0].id, this._fetchPolicies(this._selectedNetwork, s));
      } catch (i) {
        this._error = `Failed to fetch Meraki data: ${i.message || i}`;
      } finally {
        this._loading = !1;
      }
    }
  }
  async _fetchSSIDs() {
  }
  async _fetchPolicies(t, i) {
    var s;
    if (this.hass)
      try {
        let n = i || ((s = this._config) == null ? void 0 : s.config_entry_id);
        if (!n) {
          const o = await this.hass.callWS({
            type: "config_entries/get",
            domain: "meraki_ha"
          });
          n = o.length > 0 ? o[0].entry_id : void 0;
        }
        if (!n) return;
        const r = await Gt(this.hass, {
          type: kt.TIMED_ACCESS_GET_POLICIES,
          config_entry_id: n,
          network_id: t
        });
        this._policies = Array.isArray(r) ? r : (r == null ? void 0 : r.policies) || [];
      } catch (n) {
        console.error("Failed to fetch policies:", n), this._policies = [];
      }
  }
  render() {
    var i, s;
    if (this._loading && !this._networks.length)
      return v`
        <ha-card .header="${((i = this._config) == null ? void 0 : i.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    const t = (this._ssids || []).filter((n) => n.networkId === this._selectedNetwork);
    return v`
      <ha-card .header="${((s = this._config) == null ? void 0 : s.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? v`
                <ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => this._error = null}">
                  ${this._error}
                </ha-alert>
              ` : ""}
          ${this._success ? v`
                <ha-alert alert-type="success" dismissable @alert-dismissed-clicked="${() => this._success = null}">
                  ${this._success}
                </ha-alert>
              ` : ""}

          <div class="form-container">
            <ha-select
              label="Network"
              .value=${this._selectedNetwork}
              @closed=${this._handleNetworkChange}
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(this._networks || []).map(
      (n) => v`
                  <ha-list-item .value=${n.id}>
                    ${n.name}
                  </ha-list-item>
                `
    )}
            </ha-select>

            <ha-select
              label="SSID"
              .value=${this._selectedSSID}
              .disabled=${!this._selectedNetwork}
              @closed=${this._handleSSIDChange}
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(t || []).map(
      (n) => v`
                  <ha-list-item .value=${String(n.number)}>
                    ${n.name} (SSID ${n.number})
                  </ha-list-item>
                `
    )}
            </ha-select>

            <ha-select
              label="Group Policy"
              .value=${this._selectedPolicy}
              .disabled=${!this._selectedNetwork}
              @closed=${this._handlePolicyChange}
              fixedMenuPosition
              naturalMenuWidth
            >
              <ha-list-item value="">None (Default)</ha-list-item>
              ${(this._policies || []).map(
      (n) => v`
                  <ha-list-item .value=${String(n.groupPolicyId)}>
                    ${n.name}
                  </ha-list-item>
                `
    )}
            </ha-select>

            <ha-select
              label="Duration"
              .value=${this._selectedDuration}
              @closed=${this._handleDurationChange}
              fixedMenuPosition
              naturalMenuWidth
            >
              <ha-list-item value="30">30 Minutes</ha-list-item>
              <ha-list-item value="60">1 Hour</ha-list-item>
              <ha-list-item value="240">4 Hours</ha-list-item>
              <ha-list-item value="1440">24 Hours</ha-list-item>
              <ha-list-item value="10080">7 Days</ha-list-item>
            </ha-select>

            <ha-textfield
              label="Name (Optional)"
              placeholder="e.g. Guest-John"
              .value=${this._customName}
              @input=${(n) => this._customName = n.target.value}
            ></ha-textfield>

            <ha-textfield
              label="Passphrase (Optional)"
              placeholder="Leave empty to auto-generate"
              .value=${this._customPassphrase}
              @input=${(n) => this._customPassphrase = n.target.value}
            ></ha-textfield>

            <ha-button
              raised
              .disabled=${this._creating || !this._selectedNetwork || !this._selectedSSID}
              @click=${this._handleCreate}
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
    const i = t.target;
    this._selectedSSID = i.value;
  }
  _handlePolicyChange(t) {
    t.stopPropagation();
    const i = t.target;
    this._selectedPolicy = i.value;
  }
  _handleDurationChange(t) {
    t.stopPropagation();
    const i = t.target;
    this._selectedDuration = i.value;
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
oe.styles = F`
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
let $ = oe;
P([
  U({ attribute: !1 })
], $.prototype, "hass");
P([
  E()
], $.prototype, "_config");
P([
  E()
], $.prototype, "_selectedNetwork");
P([
  E()
], $.prototype, "_selectedSSID");
P([
  E()
], $.prototype, "_selectedPolicy");
P([
  E()
], $.prototype, "_selectedDuration");
P([
  E()
], $.prototype, "_customName");
P([
  E()
], $.prototype, "_customPassphrase");
P([
  E()
], $.prototype, "_creating");
P([
  E()
], $.prototype, "_error");
P([
  E()
], $.prototype, "_success");
P([
  E()
], $.prototype, "_networks");
P([
  E()
], $.prototype, "_ssids");
P([
  E()
], $.prototype, "_policies");
P([
  E()
], $.prototype, "_loading");
P([
  E()
], $.prototype, "_initDone");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", $);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: !0
});
export {
  $ as MerakiGuestAccessCard
};
