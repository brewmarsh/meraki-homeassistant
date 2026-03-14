/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ct = globalThis, Yt = Ct.ShadowRoot && (Ct.ShadyCSS === void 0 || Ct.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Qt = Symbol(), fe = /* @__PURE__ */ new WeakMap();
let Pe = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== Qt) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Yt && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = fe.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && fe.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const Ze = (n) => new Pe(typeof n == "string" ? n : n + "", void 0, Qt), H = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((s, i, r) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + n[r + 1], n[0]);
  return new Pe(e, n, Qt);
}, Xe = (n, t) => {
  if (Yt) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), i = Ct.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = e.cssText, n.appendChild(s);
  }
}, ge = Yt ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return Ze(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: ti, defineProperty: ei, getOwnPropertyDescriptor: ii, getOwnPropertyNames: si, getOwnPropertySymbols: ni, getPrototypeOf: ri } = Object, K = globalThis, pe = K.trustedTypes, oi = pe ? pe.emptyScript : "", Lt = K.reactiveElementPolyfillSupport, lt = (n, t) => n, $t = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? oi : null;
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
} }, Zt = (n, t) => !ti(n, t), me = { attribute: !0, type: String, converter: $t, reflect: !1, useDefault: !1, hasChanged: Zt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), K.litPropertyMetadata ?? (K.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let X = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = me) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(t, s, e);
      i !== void 0 && ei(this.prototype, t, i);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: i, set: r } = ii(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: i, set(o) {
      const c = i == null ? void 0 : i.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, c, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? me;
  }
  static _$Ei() {
    if (this.hasOwnProperty(lt("elementProperties"))) return;
    const t = ri(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(lt("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(lt("properties"))) {
      const e = this.properties, s = [...si(e), ...ni(e)];
      for (const i of s) this.createProperty(i, e[i]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [s, i] of e) this.elementProperties.set(s, i);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, s] of this.elementProperties) {
      const i = this._$Eu(e, s);
      i !== void 0 && this._$Eh.set(i, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const s = new Set(t.flat(1 / 0).reverse());
      for (const i of s) e.unshift(ge(i));
    } else t !== void 0 && e.push(ge(t));
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
    return Xe(t, this.constructor.elementStyles), t;
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
    const s = this.constructor.elementProperties.get(t), i = this.constructor._$Eu(t, s);
    if (i !== void 0 && s.reflect === !0) {
      const o = (((r = s.converter) == null ? void 0 : r.toAttribute) !== void 0 ? s.converter : $t).toAttribute(e, s.type);
      this._$Em = t, o == null ? this.removeAttribute(i) : this.setAttribute(i, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const s = this.constructor, i = s._$Eh.get(t);
    if (i !== void 0 && this._$Em !== i) {
      const c = s.getPropertyOptions(i), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((r = c.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? c.converter : $t;
      this._$Em = i;
      const l = a.fromAttribute(e, c.type);
      this[i] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(i)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, i = !1, r) {
    var o;
    if (t !== void 0) {
      const c = this.constructor;
      if (i === !1 && (r = this[t]), s ?? (s = c.getPropertyOptions(t)), !((s.hasChanged ?? Zt)(r, e) || s.useDefault && s.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(c._$Eu(t, s)))) return;
      this.C(t, e, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: s, reflect: i, wrapped: r }, o) {
    s && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || s || (e = void 0), this._$AL.set(t, e)), i === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
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
      const i = this.constructor.elementProperties;
      if (i.size > 0) for (const [r, o] of i) {
        const { wrapped: c } = o, a = this[r];
        c !== !0 || this._$AL.has(r) || a === void 0 || this.C(r, void 0, o, a);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (s = this._$EO) == null || s.forEach((i) => {
        var r;
        return (r = i.hostUpdate) == null ? void 0 : r.call(i);
      }), this.update(e)) : this._$EM();
    } catch (i) {
      throw t = !1, this._$EM(), i;
    }
    t && this._$AE(e);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var e;
    (e = this._$EO) == null || e.forEach((s) => {
      var i;
      return (i = s.hostUpdated) == null ? void 0 : i.call(s);
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
X.elementStyles = [], X.shadowRootOptions = { mode: "open" }, X[lt("elementProperties")] = /* @__PURE__ */ new Map(), X[lt("finalized")] = /* @__PURE__ */ new Map(), Lt == null || Lt({ ReactiveElement: X }), (K.reactiveElementVersions ?? (K.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const dt = globalThis, _e = (n) => n, St = dt.trustedTypes, ye = St ? St.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, Te = "$lit$", j = `lit$${Math.random().toFixed(9).slice(2)}$`, Ne = "?" + j, ai = `<${Ne}>`, Q = document, ut = () => Q.createComment(""), ft = (n) => n === null || typeof n != "object" && typeof n != "function", Xt = Array.isArray, ci = (n) => Xt(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", Ut = `[ 	
\f\r]`, ct = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, we = /-->/g, ve = />/g, J = RegExp(`>|${Ut}(?:([^\\s"'>=/]+)(${Ut}*=${Ut}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), be = /'/g, Ee = /"/g, Ie = /^(?:script|style|textarea|title)$/i, li = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), b = li(1), tt = Symbol.for("lit-noChange"), $ = Symbol.for("lit-nothing"), Ae = /* @__PURE__ */ new WeakMap(), W = Q.createTreeWalker(Q, 129);
function Me(n, t) {
  if (!Xt(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ye !== void 0 ? ye.createHTML(t) : t;
}
const di = (n, t) => {
  const e = n.length - 1, s = [];
  let i, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = ct;
  for (let c = 0; c < e; c++) {
    const a = n[c];
    let l, d, u = -1, f = 0;
    for (; f < a.length && (o.lastIndex = f, d = o.exec(a), d !== null); ) f = o.lastIndex, o === ct ? d[1] === "!--" ? o = we : d[1] !== void 0 ? o = ve : d[2] !== void 0 ? (Ie.test(d[2]) && (i = RegExp("</" + d[2], "g")), o = J) : d[3] !== void 0 && (o = J) : o === J ? d[0] === ">" ? (o = i ?? ct, u = -1) : d[1] === void 0 ? u = -2 : (u = o.lastIndex - d[2].length, l = d[1], o = d[3] === void 0 ? J : d[3] === '"' ? Ee : be) : o === Ee || o === be ? o = J : o === we || o === ve ? o = ct : (o = J, i = void 0);
    const h = o === J && n[c + 1].startsWith("/>") ? " " : "";
    r += o === ct ? a + ai : u >= 0 ? (s.push(l), a.slice(0, u) + Te + a.slice(u) + j + h) : a + j + (u === -2 ? c : h);
  }
  return [Me(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class gt {
  constructor({ strings: t, _$litType$: e }, s) {
    let i;
    this.parts = [];
    let r = 0, o = 0;
    const c = t.length - 1, a = this.parts, [l, d] = di(t, e);
    if (this.el = gt.createElement(l, s), W.currentNode = this.el.content, e === 2 || e === 3) {
      const u = this.el.content.firstChild;
      u.replaceWith(...u.childNodes);
    }
    for (; (i = W.nextNode()) !== null && a.length < c; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const u of i.getAttributeNames()) if (u.endsWith(Te)) {
          const f = d[o++], h = i.getAttribute(u).split(j), g = /([.?@])?(.*)/.exec(f);
          a.push({ type: 1, index: r, name: g[2], strings: h, ctor: g[1] === "." ? ui : g[1] === "?" ? fi : g[1] === "@" ? gi : Tt }), i.removeAttribute(u);
        } else u.startsWith(j) && (a.push({ type: 6, index: r }), i.removeAttribute(u));
        if (Ie.test(i.tagName)) {
          const u = i.textContent.split(j), f = u.length - 1;
          if (f > 0) {
            i.textContent = St ? St.emptyScript : "";
            for (let h = 0; h < f; h++) i.append(u[h], ut()), W.nextNode(), a.push({ type: 2, index: ++r });
            i.append(u[f], ut());
          }
        }
      } else if (i.nodeType === 8) if (i.data === Ne) a.push({ type: 2, index: r });
      else {
        let u = -1;
        for (; (u = i.data.indexOf(j, u + 1)) !== -1; ) a.push({ type: 7, index: r }), u += j.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const s = Q.createElement("template");
    return s.innerHTML = t, s;
  }
}
function et(n, t, e = n, s) {
  var o, c;
  if (t === tt) return t;
  let i = s !== void 0 ? (o = e._$Co) == null ? void 0 : o[s] : e._$Cl;
  const r = ft(t) ? void 0 : t._$litDirective$;
  return (i == null ? void 0 : i.constructor) !== r && ((c = i == null ? void 0 : i._$AO) == null || c.call(i, !1), r === void 0 ? i = void 0 : (i = new r(n), i._$AT(n, e, s)), s !== void 0 ? (e._$Co ?? (e._$Co = []))[s] = i : e._$Cl = i), i !== void 0 && (t = et(n, i._$AS(n, t.values), i, s)), t;
}
class hi {
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
    const { el: { content: e }, parts: s } = this._$AD, i = ((t == null ? void 0 : t.creationScope) ?? Q).importNode(e, !0);
    W.currentNode = i;
    let r = W.nextNode(), o = 0, c = 0, a = s[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let l;
        a.type === 2 ? l = new wt(r, r.nextSibling, this, t) : a.type === 1 ? l = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (l = new pi(r, this, t)), this._$AV.push(l), a = s[++c];
      }
      o !== (a == null ? void 0 : a.index) && (r = W.nextNode(), o++);
    }
    return W.currentNode = Q, i;
  }
  p(t) {
    let e = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, e), e += s.strings.length - 2) : s._$AI(t[e])), e++;
  }
}
class wt {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, s, i) {
    this.type = 2, this._$AH = $, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = i, this._$Cv = (i == null ? void 0 : i.isConnected) ?? !0;
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
    t = et(this, t, e), ft(t) ? t === $ || t == null || t === "" ? (this._$AH !== $ && this._$AR(), this._$AH = $) : t !== this._$AH && t !== tt && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : ci(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== $ && ft(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Q.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: s } = t, i = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = gt.createElement(Me(s.h, s.h[0]), this.options)), s);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === i) this._$AH.p(e);
    else {
      const o = new hi(i, this), c = o.u(this.options);
      o.p(e), this.T(c), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = Ae.get(t.strings);
    return e === void 0 && Ae.set(t.strings, e = new gt(t)), e;
  }
  k(t) {
    Xt(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, i = 0;
    for (const r of t) i === e.length ? e.push(s = new wt(this.O(ut()), this.O(ut()), this, this.options)) : s = e[i], s._$AI(r), i++;
    i < e.length && (this._$AR(s && s._$AB.nextSibling, i), e.length = i);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, e); t !== this._$AB; ) {
      const i = _e(t).nextSibling;
      _e(t).remove(), t = i;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class Tt {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, s, i, r) {
    this.type = 1, this._$AH = $, this._$AN = void 0, this.element = t, this.name = e, this._$AM = i, this.options = r, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = $;
  }
  _$AI(t, e = this, s, i) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = et(this, t, e, 0), o = !ft(t) || t !== this._$AH && t !== tt, o && (this._$AH = t);
    else {
      const c = t;
      let a, l;
      for (t = r[0], a = 0; a < r.length - 1; a++) l = et(this, c[s + a], e, a), l === tt && (l = this._$AH[a]), o || (o = !ft(l) || l !== this._$AH[a]), l === $ ? t = $ : t !== $ && (t += (l ?? "") + r[a + 1]), this._$AH[a] = l;
    }
    o && !i && this.j(t);
  }
  j(t) {
    t === $ ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class ui extends Tt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === $ ? void 0 : t;
  }
}
class fi extends Tt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== $);
  }
}
class gi extends Tt {
  constructor(t, e, s, i, r) {
    super(t, e, s, i, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = et(this, t, e, 0) ?? $) === tt) return;
    const s = this._$AH, i = t === $ && s !== $ || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, r = t !== $ && (s === $ || i);
    i && this.element.removeEventListener(this.name, this, s), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class pi {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    et(this, t);
  }
}
const Ot = dt.litHtmlPolyfillSupport;
Ot == null || Ot(gt, wt), (dt.litHtmlVersions ?? (dt.litHtmlVersions = [])).push("3.3.2");
const mi = (n, t, e) => {
  const s = (e == null ? void 0 : e.renderBefore) ?? t;
  let i = s._$litPart$;
  if (i === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    s._$litPart$ = i = new wt(t.insertBefore(ut(), r), r, void 0, e ?? {});
  }
  return i._$AI(n), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Y = globalThis;
class T extends X {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = mi(e, this.renderRoot, this.renderOptions);
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
    return tt;
  }
}
var ke;
T._$litElement$ = !0, T.finalized = !0, (ke = Y.litElementHydrateSupport) == null || ke.call(Y, { LitElement: T });
const Ht = Y.litElementPolyfillSupport;
Ht == null || Ht({ LitElement: T });
(Y.litElementVersions ?? (Y.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const _i = { attribute: !0, type: String, converter: $t, reflect: !1, hasChanged: Zt }, yi = (n = _i, t, e) => {
  const { kind: s, metadata: i } = e;
  let r = globalThis.litPropertyMetadata.get(i);
  if (r === void 0 && globalThis.litPropertyMetadata.set(i, r = /* @__PURE__ */ new Map()), s === "setter" && ((n = Object.create(n)).wrapped = !0), r.set(e.name, n), s === "accessor") {
    const { name: o } = e;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(o, a, n, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(o, void 0, n, c), c;
    } };
  }
  if (s === "setter") {
    const { name: o } = e;
    return function(c) {
      const a = this[o];
      t.call(this, c), this.requestUpdate(o, a, n, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + s);
};
function z(n) {
  return (t, e) => typeof e == "object" ? yi(n, t, e) : ((s, i, r) => {
    const o = i.hasOwnProperty(r);
    return i.constructor.createProperty(r, s), o ? Object.getOwnPropertyDescriptor(i, r) : void 0;
  })(n, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function v(n) {
  return z({ ...n, state: !0, attribute: !1 });
}
const xe = (n, t, e) => b`
  <ha-card class="status-card warning">
    <div class="card-content flex-col align-center p-8">
      <ha-icon icon="mdi:alert-circle" style="--mdc-icon-size: 48px; margin-bottom: 16px;"></ha-icon>
      <h1 class="status-title">${n}</h1>
      <div class="status-message mt-4">${t}</div>
    </div>
    ${b`<div class="version">v${e}</div>`}
  </ha-card>
`, Nt = (n, t, e) => b`
  <ha-card class="status-card loading">
    <div class="card-content flex-col align-center p-8">
      <h1 class="status-title">${n}</h1>
      <ha-circular-progress active></ha-circular-progress>
      <div class="status-message mt-4">${t}</div>
    </div>
    <div class="version">v${e}</div>
  </ha-card>
`, It = H`
  ha-card.status-card {
    --ha-card-background: var(--warning-color, #ffeb3b);
    background-color: var(--warning-color, #ffeb3b) !important;
    border-radius: 12px;
    overflow: hidden;
  }
  ha-card.status-card.loading {
    --ha-card-background: var(--info-color, #2196f3);
    background-color: var(--info-color, #2196f3) !important;
  }
  ha-card.status-card.warning {
    --ha-card-background: var(--warning-color, #ffeb3b);
    background-color: var(--warning-color, #ffeb3b) !important;
  }

  /* Force high-contrast dark text on bright colored backgrounds in light mode */
  .status-card .status-title,
  .status-card .status-message {
    color: #111111 !important;
    text-align: center;
  }

  .status-card .status-title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
  }

  @media (prefers-color-scheme: dark) {
    ha-card.status-card.warning {
      --ha-card-background: rgba(255, 193, 7, 0.2);
      background-color: rgba(255, 193, 7, 0.2) !important;
    }
    ha-card.status-card.loading {
      --ha-card-background: rgba(33, 150, 243, 0.2);
      background-color: rgba(33, 150, 243, 0.2) !important;
    }
    .status-card .status-title,
    .status-card .status-message {
      color: var(--primary-text-color) !important;
    }
  }

  .flex-col { display: flex; flex-direction: column; }
  .align-center { align-items: center; }
  .p-8 { padding: 32px; }
  .mt-4 { margin-top: 16px; }

  .version {
    font-size: 9px;
    color: var(--secondary-text-color);
    text-align: right;
    padding: 4px 12px;
    opacity: 0.4;
  }

  /* Legacy styles for backward compatibility during transition */
  .meraki-warning {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    background-color: var(--warning-color);
    color: var(--primary-text-color);
    border-radius: 8px;
  }
  .meraki-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    gap: 12px;
  }
`;
var De = /* @__PURE__ */ ((n) => (n.GET_CONFIG = "meraki_ha/get_config", n.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", n.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", n.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", n.GET_VERSION = "meraki_ha/get_version", n.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", n.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", n.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", n.GET_GUEST_KEYS = "meraki_ha/ipsk/get", n.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", n.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", n))(De || {});
const wi = async (n, t) => {
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
class R {
  /**
   * Fetches wireless networks, SSIDs, and group policies directly from the integration's backend cache.
   */
  static async fetchConfig(t) {
    try {
      const e = await t.callWS({
        type: "config_entries/get",
        domain: "meraki_ha"
      }), s = e.length > 0 ? e[0].entry_id : null;
      if (!s)
        return { networks: [], ssids: [], groupPolicies: [], entryId: null };
      const i = await wi(t, {
        type: De.GET_CONFIG,
        config_entry_id: s
      }), r = (Array.isArray(i.networks) ? i.networks : []).filter((a) => {
        var l;
        return (l = a.productTypes) == null ? void 0 : l.includes("wireless");
      }), o = Array.isArray(i.ssids) ? i.ssids : [], c = [];
      if (i.group_policies && typeof i.group_policies == "object")
        for (const [a, l] of Object.entries(
          i.group_policies
        ))
          Array.isArray(l) && l.forEach((d) => {
            c.push({
              networkId: a,
              groupPolicyId: String(d.groupPolicyId),
              name: d.name
            });
          });
      return { networks: r, ssids: o, groupPolicies: c, entryId: s };
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
  static async pollConfig(t, e, s = 12, i = 5e3) {
    for (let r = 0; r < s; r++) {
      try {
        const o = await this.fetchConfig(t);
        if (o.networks.length > 0)
          return e("", !1), o;
        e(
          `Waiting for integration to sync... (Attempt ${r + 1}/${s})`,
          !0
        );
      } catch {
        e(
          `Error connecting to backend. Retrying... (Attempt ${r + 1}/${s})`,
          !0
        );
      }
      await new Promise((o) => setTimeout(o, i));
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
    const s = t.map((i) => ({ value: i.id, label: i.name }));
    return e ? [{ value: "", label: "All Networks" }, ...s] : s;
  }
  /**
   * Formats SSIDs for an ha-form dropdown.
   * @param valueType Determines if the dropdown returns the SSID's string name (for QR codes) or integer number (for Guest API calls).
   */
  static getSsidOptions(t, e, s = "name") {
    return (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: s === "number" ? String(r.number) : r.name,
      label: `${r.name} (SSID ${r.number})`
    }));
  }
  /**
   * Formats Group Policies for an ha-form dropdown.
   */
  static getGroupPolicyOptions(t, e) {
    const i = (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: r.groupPolicyId,
      label: r.name
    }));
    return [
      { value: "CREATE", label: "Create 'Home Assistant Guest' Policy" },
      { value: "NONE", label: "None (Network Default)" },
      ...i
    ];
  }
}
var vi = Object.defineProperty, G = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && vi(t, e, i), i;
};
const re = class re extends T {
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
    this.hass && await R.pollConfig(
      this.hass,
      (t, e) => {
        this._loadingMessage = t, this._isLoading = e;
      }
    );
  }
  _discoverEntity() {
    if (this.hass)
      return Object.keys(this.hass.states).find((t) => {
        var i;
        if (!t.startsWith("select.")) return !1;
        const s = ((i = this.hass.states[t].attributes.friendly_name) == null ? void 0 : i.toLowerCase()) || "";
        return t.includes("content_filter") || s.includes("content filter") || t.includes("meraki");
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
    if (!this.hass || !this._config) return b``;
    if (this._isLoading)
      return Nt(
        ((l = this._config) == null ? void 0 : l.name) || "Meraki Content Filter",
        this._loadingMessage,
        "2.3.0-beta.3504"
      );
    const t = this._config.entity || this._discoverEntity(), e = t ? this.hass.states[t] : void 0, s = this._config.entity ? this.hass.states[this._config.entity] : void 0, i = ((d = s == null ? void 0 : s.attributes) == null ? void 0 : d.friendly_name) || "Meraki", r = this._config.name || (this._config.entity ? `${i} Content Filter` : "Meraki Content Filter");
    if (!t || !e)
      return xe(
        "Entity Missing",
        "No content filter entity was found. Please check your configuration.",
        "2.3.0-beta.3504"
      );
    const o = e.state || "Unknown", c = ((u = e.attributes) == null ? void 0 : u.options) || ["None", "Security", "Family", "Strict"], a = this._optimisticProfile || o;
    return b`
      <ha-card .header="${r}">
        <div class="card-content">
          <div class="button-grid">
            ${c.map((f) => {
      const h = a.toLowerCase() === f.toLowerCase(), g = this._isUpdating && this._optimisticProfile === f;
      return b`
                <button
                  class="filter-btn ${h ? "active" : ""} ${this._isUpdating && !g ? "disabled" : ""}"
                  ?disabled=${this._isUpdating}
                  @click=${() => this._setFilterProfile(f, t)}
                >
                  ${g ? b`<ha-circular-progress active size="small"></ha-circular-progress> Saving...` : f}
                </button>
              `;
    })}
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3504"}</div>
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
      } catch (s) {
        console.error("Failed to call select_option service:", s), this._optimisticProfile = null, this._isUpdating = !1;
      }
    }
  }
};
re.styles = [
  It,
  H`
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
let L = re;
G([
  z({ attribute: !1 })
], L.prototype, "hass");
G([
  v()
], L.prototype, "_config");
G([
  v()
], L.prototype, "_optimisticProfile");
G([
  v()
], L.prototype, "_isUpdating");
G([
  v()
], L.prototype, "_isLoading");
G([
  v()
], L.prototype, "_loadingMessage");
const oe = class oe extends T {
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
    return !this.hass || !this._config ? b`` : b`
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
oe.styles = H`
    .editor-container { padding: 16px; }
  `;
let pt = oe;
G([
  z({ attribute: !1 })
], pt.prototype, "hass");
G([
  v()
], pt.prototype, "_config");
customElements.get("meraki-content-filter-card") || customElements.define("meraki-content-filter-card", L);
customElements.get("meraki-content-filter-card-editor") || customElements.define("meraki-content-filter-card-editor", pt);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-content-filter-card") || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var vt = {}, bi = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, Be = {}, P = {};
let te;
const Ei = [
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
P.getSymbolSize = function(t) {
  if (!t) throw new Error('"version" cannot be null or undefined');
  if (t < 1 || t > 40) throw new Error('"version" should be in range from 1 to 40');
  return t * 4 + 17;
};
P.getSymbolTotalCodewords = function(t) {
  return Ei[t];
};
P.getBCHDigit = function(n) {
  let t = 0;
  for (; n !== 0; )
    t++, n >>>= 1;
  return t;
};
P.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  te = t;
};
P.isKanjiModeEnabled = function() {
  return typeof te < "u";
};
P.toSJIS = function(t) {
  return te(t);
};
var Mt = {};
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
  n.isValid = function(s) {
    return s && typeof s.bit < "u" && s.bit >= 0 && s.bit < 4;
  }, n.from = function(s, i) {
    if (n.isValid(s))
      return s;
    try {
      return t(s);
    } catch {
      return i;
    }
  };
})(Mt);
function Re() {
  this.buffer = [], this.length = 0;
}
Re.prototype = {
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
var Ai = Re;
function bt(n) {
  if (!n || n < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = n, this.data = new Uint8Array(n * n), this.reservedBit = new Uint8Array(n * n);
}
bt.prototype.set = function(n, t, e, s) {
  const i = n * this.size + t;
  this.data[i] = e, s && (this.reservedBit[i] = !0);
};
bt.prototype.get = function(n, t) {
  return this.data[n * this.size + t];
};
bt.prototype.xor = function(n, t, e) {
  this.data[n * this.size + t] ^= e;
};
bt.prototype.isReserved = function(n, t) {
  return this.reservedBit[n * this.size + t];
};
var Ci = bt, Le = {};
(function(n) {
  const t = P.getSymbolSize;
  n.getRowColCoords = function(s) {
    if (s === 1) return [];
    const i = Math.floor(s / 7) + 2, r = t(s), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * i - 2)) * 2, c = [r - 7];
    for (let a = 1; a < i - 1; a++)
      c[a] = c[a - 1] - o;
    return c.push(6), c.reverse();
  }, n.getPositions = function(s) {
    const i = [], r = n.getRowColCoords(s), o = r.length;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        c === 0 && a === 0 || // top-left
        c === 0 && a === o - 1 || // bottom-left
        c === o - 1 && a === 0 || i.push([r[c], r[a]]);
    return i;
  };
})(Le);
var Ue = {};
const $i = P.getSymbolSize, Ce = 7;
Ue.getPositions = function(t) {
  const e = $i(t);
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
  n.isValid = function(i) {
    return i != null && i !== "" && !isNaN(i) && i >= 0 && i <= 7;
  }, n.from = function(i) {
    return n.isValid(i) ? parseInt(i, 10) : void 0;
  }, n.getPenaltyN1 = function(i) {
    const r = i.size;
    let o = 0, c = 0, a = 0, l = null, d = null;
    for (let u = 0; u < r; u++) {
      c = a = 0, l = d = null;
      for (let f = 0; f < r; f++) {
        let h = i.get(u, f);
        h === l ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), l = h, c = 1), h = i.get(f, u), h === d ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), d = h, a = 1);
      }
      c >= 5 && (o += t.N1 + (c - 5)), a >= 5 && (o += t.N1 + (a - 5));
    }
    return o;
  }, n.getPenaltyN2 = function(i) {
    const r = i.size;
    let o = 0;
    for (let c = 0; c < r - 1; c++)
      for (let a = 0; a < r - 1; a++) {
        const l = i.get(c, a) + i.get(c, a + 1) + i.get(c + 1, a) + i.get(c + 1, a + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, n.getPenaltyN3 = function(i) {
    const r = i.size;
    let o = 0, c = 0, a = 0;
    for (let l = 0; l < r; l++) {
      c = a = 0;
      for (let d = 0; d < r; d++)
        c = c << 1 & 2047 | i.get(l, d), d >= 10 && (c === 1488 || c === 93) && o++, a = a << 1 & 2047 | i.get(d, l), d >= 10 && (a === 1488 || a === 93) && o++;
    }
    return o * t.N3;
  }, n.getPenaltyN4 = function(i) {
    let r = 0;
    const o = i.data.length;
    for (let a = 0; a < o; a++) r += i.data[a];
    return Math.abs(Math.ceil(r * 100 / o / 5) - 10) * t.N4;
  };
  function e(s, i, r) {
    switch (s) {
      case n.Patterns.PATTERN000:
        return (i + r) % 2 === 0;
      case n.Patterns.PATTERN001:
        return i % 2 === 0;
      case n.Patterns.PATTERN010:
        return r % 3 === 0;
      case n.Patterns.PATTERN011:
        return (i + r) % 3 === 0;
      case n.Patterns.PATTERN100:
        return (Math.floor(i / 2) + Math.floor(r / 3)) % 2 === 0;
      case n.Patterns.PATTERN101:
        return i * r % 2 + i * r % 3 === 0;
      case n.Patterns.PATTERN110:
        return (i * r % 2 + i * r % 3) % 2 === 0;
      case n.Patterns.PATTERN111:
        return (i * r % 3 + (i + r) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + s);
    }
  }
  n.applyMask = function(i, r) {
    const o = r.size;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        r.isReserved(a, c) || r.xor(a, c, e(i, a, c));
  }, n.getBestMask = function(i, r) {
    const o = Object.keys(n.Patterns).length;
    let c = 0, a = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), n.applyMask(l, i);
      const d = n.getPenaltyN1(i) + n.getPenaltyN2(i) + n.getPenaltyN3(i) + n.getPenaltyN4(i);
      n.applyMask(l, i), d < a && (a = d, c = l);
    }
    return c;
  };
})(Oe);
var xt = {};
const V = Mt, Et = [
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
], At = [
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
    case V.L:
      return Et[(t - 1) * 4 + 0];
    case V.M:
      return Et[(t - 1) * 4 + 1];
    case V.Q:
      return Et[(t - 1) * 4 + 2];
    case V.H:
      return Et[(t - 1) * 4 + 3];
    default:
      return;
  }
};
xt.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case V.L:
      return At[(t - 1) * 4 + 0];
    case V.M:
      return At[(t - 1) * 4 + 1];
    case V.Q:
      return At[(t - 1) * 4 + 2];
    case V.H:
      return At[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var He = {}, Dt = {};
const ht = new Uint8Array(512), kt = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    ht[e] = t, kt[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    ht[e] = ht[e - 255];
})();
Dt.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return kt[t];
};
Dt.exp = function(t) {
  return ht[t];
};
Dt.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : ht[kt[t] + kt[e]];
};
(function(n) {
  const t = Dt;
  n.mul = function(s, i) {
    const r = new Uint8Array(s.length + i.length - 1);
    for (let o = 0; o < s.length; o++)
      for (let c = 0; c < i.length; c++)
        r[o + c] ^= t.mul(s[o], i[c]);
    return r;
  }, n.mod = function(s, i) {
    let r = new Uint8Array(s);
    for (; r.length - i.length >= 0; ) {
      const o = r[0];
      for (let a = 0; a < i.length; a++)
        r[a] ^= t.mul(i[a], o);
      let c = 0;
      for (; c < r.length && r[c] === 0; ) c++;
      r = r.slice(c);
    }
    return r;
  }, n.generateECPolynomial = function(s) {
    let i = new Uint8Array([1]);
    for (let r = 0; r < s; r++)
      i = n.mul(i, new Uint8Array([1, t.exp(r)]));
    return i;
  };
})(He);
const ze = He;
function ee(n) {
  this.genPoly = void 0, this.degree = n, this.degree && this.initialize(this.degree);
}
ee.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = ze.generateECPolynomial(this.degree);
};
ee.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const s = ze.mod(e, this.genPoly), i = this.degree - s.length;
  if (i > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(s, i), r;
  }
  return s;
};
var Si = ee, Fe = {}, q = {}, ie = {};
ie.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var D = {};
const je = "[0-9]+", ki = "[A-Z $%*+\\-./:]+";
let mt = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
mt = mt.replace(/u/g, "\\u");
const Pi = "(?:(?![A-Z0-9 $%*+\\-./:]|" + mt + `)(?:.|[\r
]))+`;
D.KANJI = new RegExp(mt, "g");
D.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
D.BYTE = new RegExp(Pi, "g");
D.NUMERIC = new RegExp(je, "g");
D.ALPHANUMERIC = new RegExp(ki, "g");
const Ti = new RegExp("^" + mt + "$"), Ni = new RegExp("^" + je + "$"), Ii = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
D.testKanji = function(t) {
  return Ti.test(t);
};
D.testNumeric = function(t) {
  return Ni.test(t);
};
D.testAlphanumeric = function(t) {
  return Ii.test(t);
};
(function(n) {
  const t = ie, e = D;
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
  function s(i) {
    if (typeof i != "string")
      throw new Error("Param is not a string");
    switch (i.toLowerCase()) {
      case "numeric":
        return n.NUMERIC;
      case "alphanumeric":
        return n.ALPHANUMERIC;
      case "kanji":
        return n.KANJI;
      case "byte":
        return n.BYTE;
      default:
        throw new Error("Unknown mode: " + i);
    }
  }
  n.from = function(r, o) {
    if (n.isValid(r))
      return r;
    try {
      return s(r);
    } catch {
      return o;
    }
  };
})(q);
(function(n) {
  const t = P, e = xt, s = Mt, i = q, r = ie, o = 7973, c = t.getBCHDigit(o);
  function a(f, h, g) {
    for (let y = 1; y <= 40; y++)
      if (h <= n.getCapacity(y, g, f))
        return y;
  }
  function l(f, h) {
    return i.getCharCountIndicator(f, h) + 4;
  }
  function d(f, h) {
    let g = 0;
    return f.forEach(function(y) {
      const S = l(y.mode, h);
      g += S + y.getBitsLength();
    }), g;
  }
  function u(f, h) {
    for (let g = 1; g <= 40; g++)
      if (d(f, g) <= n.getCapacity(g, h, i.MIXED))
        return g;
  }
  n.from = function(h, g) {
    return r.isValid(h) ? parseInt(h, 10) : g;
  }, n.getCapacity = function(h, g, y) {
    if (!r.isValid(h))
      throw new Error("Invalid QR Code version");
    typeof y > "u" && (y = i.BYTE);
    const S = t.getSymbolTotalCodewords(h), _ = e.getTotalCodewordsCount(h, g), w = (S - _) * 8;
    if (y === i.MIXED) return w;
    const m = w - l(y, h);
    switch (y) {
      case i.NUMERIC:
        return Math.floor(m / 10 * 3);
      case i.ALPHANUMERIC:
        return Math.floor(m / 11 * 2);
      case i.KANJI:
        return Math.floor(m / 13);
      case i.BYTE:
      default:
        return Math.floor(m / 8);
    }
  }, n.getBestVersionForData = function(h, g) {
    let y;
    const S = s.from(g, s.M);
    if (Array.isArray(h)) {
      if (h.length > 1)
        return u(h, S);
      if (h.length === 0)
        return 1;
      y = h[0];
    } else
      y = h;
    return a(y.mode, y.getLength(), S);
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
const Gt = P, Ke = 1335, Mi = 21522, $e = Gt.getBCHDigit(Ke);
Ve.getEncodedBits = function(t, e) {
  const s = t.bit << 3 | e;
  let i = s << 10;
  for (; Gt.getBCHDigit(i) - $e >= 0; )
    i ^= Ke << Gt.getBCHDigit(i) - $e;
  return (s << 10 | i) ^ Mi;
};
var Ge = {};
const xi = q;
function it(n) {
  this.mode = xi.NUMERIC, this.data = n.toString();
}
it.getBitsLength = function(t) {
  return 10 * Math.floor(t / 3) + (t % 3 ? t % 3 * 3 + 1 : 0);
};
it.prototype.getLength = function() {
  return this.data.length;
};
it.prototype.getBitsLength = function() {
  return it.getBitsLength(this.data.length);
};
it.prototype.write = function(t) {
  let e, s, i;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    s = this.data.substr(e, 3), i = parseInt(s, 10), t.put(i, 10);
  const r = this.data.length - e;
  r > 0 && (s = this.data.substr(e), i = parseInt(s, 10), t.put(i, r * 3 + 1));
};
var Di = it;
const Bi = q, zt = [
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
function st(n) {
  this.mode = Bi.ALPHANUMERIC, this.data = n;
}
st.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
st.prototype.getLength = function() {
  return this.data.length;
};
st.prototype.getBitsLength = function() {
  return st.getBitsLength(this.data.length);
};
st.prototype.write = function(t) {
  let e;
  for (e = 0; e + 2 <= this.data.length; e += 2) {
    let s = zt.indexOf(this.data[e]) * 45;
    s += zt.indexOf(this.data[e + 1]), t.put(s, 11);
  }
  this.data.length % 2 && t.put(zt.indexOf(this.data[e]), 6);
};
var Ri = st;
const Li = q;
function nt(n) {
  this.mode = Li.BYTE, typeof n == "string" ? this.data = new TextEncoder().encode(n) : this.data = new Uint8Array(n);
}
nt.getBitsLength = function(t) {
  return t * 8;
};
nt.prototype.getLength = function() {
  return this.data.length;
};
nt.prototype.getBitsLength = function() {
  return nt.getBitsLength(this.data.length);
};
nt.prototype.write = function(n) {
  for (let t = 0, e = this.data.length; t < e; t++)
    n.put(this.data[t], 8);
};
var Ui = nt;
const Oi = q, Hi = P;
function rt(n) {
  this.mode = Oi.KANJI, this.data = n;
}
rt.getBitsLength = function(t) {
  return t * 13;
};
rt.prototype.getLength = function() {
  return this.data.length;
};
rt.prototype.getBitsLength = function() {
  return rt.getBitsLength(this.data.length);
};
rt.prototype.write = function(n) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let e = Hi.toSJIS(this.data[t]);
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
var zi = rt, qe = { exports: {} };
(function(n) {
  var t = {
    single_source_shortest_paths: function(e, s, i) {
      var r = {}, o = {};
      o[s] = 0;
      var c = t.PriorityQueue.make();
      c.push(s, 0);
      for (var a, l, d, u, f, h, g, y, S; !c.empty(); ) {
        a = c.pop(), l = a.value, u = a.cost, f = e[l] || {};
        for (d in f)
          f.hasOwnProperty(d) && (h = f[d], g = u + h, y = o[d], S = typeof o[d] > "u", (S || y > g) && (o[d] = g, c.push(d, g), r[d] = l));
      }
      if (typeof i < "u" && typeof o[i] > "u") {
        var _ = ["Could not find a path from ", s, " to ", i, "."].join("");
        throw new Error(_);
      }
      return r;
    },
    extract_shortest_path_from_predecessor_list: function(e, s) {
      for (var i = [], r = s; r; )
        i.push(r), e[r], r = e[r];
      return i.reverse(), i;
    },
    find_path: function(e, s, i) {
      var r = t.single_source_shortest_paths(e, s, i);
      return t.extract_shortest_path_from_predecessor_list(
        r,
        i
      );
    },
    /**
     * A very naive priority queue implementation.
     */
    PriorityQueue: {
      make: function(e) {
        var s = t.PriorityQueue, i = {}, r;
        e = e || {};
        for (r in s)
          s.hasOwnProperty(r) && (i[r] = s[r]);
        return i.queue = [], i.sorter = e.sorter || s.default_sorter, i;
      },
      default_sorter: function(e, s) {
        return e.cost - s.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(e, s) {
        var i = { value: e, cost: s };
        this.queue.push(i), this.queue.sort(this.sorter);
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
var Fi = qe.exports;
(function(n) {
  const t = q, e = Di, s = Ri, i = Ui, r = zi, o = D, c = P, a = Fi;
  function l(_) {
    return unescape(encodeURIComponent(_)).length;
  }
  function d(_, w, m) {
    const p = [];
    let E;
    for (; (E = _.exec(m)) !== null; )
      p.push({
        data: E[0],
        index: E.index,
        mode: w,
        length: E[0].length
      });
    return p;
  }
  function u(_) {
    const w = d(o.NUMERIC, t.NUMERIC, _), m = d(o.ALPHANUMERIC, t.ALPHANUMERIC, _);
    let p, E;
    return c.isKanjiModeEnabled() ? (p = d(o.BYTE, t.BYTE, _), E = d(o.KANJI, t.KANJI, _)) : (p = d(o.BYTE_KANJI, t.BYTE, _), E = []), w.concat(m, p, E).sort(function(C, M) {
      return C.index - M.index;
    }).map(function(C) {
      return {
        data: C.data,
        mode: C.mode,
        length: C.length
      };
    });
  }
  function f(_, w) {
    switch (w) {
      case t.NUMERIC:
        return e.getBitsLength(_);
      case t.ALPHANUMERIC:
        return s.getBitsLength(_);
      case t.KANJI:
        return r.getBitsLength(_);
      case t.BYTE:
        return i.getBitsLength(_);
    }
  }
  function h(_) {
    return _.reduce(function(w, m) {
      const p = w.length - 1 >= 0 ? w[w.length - 1] : null;
      return p && p.mode === m.mode ? (w[w.length - 1].data += m.data, w) : (w.push(m), w);
    }, []);
  }
  function g(_) {
    const w = [];
    for (let m = 0; m < _.length; m++) {
      const p = _[m];
      switch (p.mode) {
        case t.NUMERIC:
          w.push([
            p,
            { data: p.data, mode: t.ALPHANUMERIC, length: p.length },
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          w.push([
            p,
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.KANJI:
          w.push([
            p,
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
          break;
        case t.BYTE:
          w.push([
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
      }
    }
    return w;
  }
  function y(_, w) {
    const m = {}, p = { start: {} };
    let E = ["start"];
    for (let A = 0; A < _.length; A++) {
      const C = _[A], M = [];
      for (let F = 0; F < C.length; F++) {
        const x = C[F], at = "" + A + F;
        M.push(at), m[at] = { node: x, lastCount: 0 }, p[at] = {};
        for (let Rt = 0; Rt < E.length; Rt++) {
          const B = E[Rt];
          m[B] && m[B].node.mode === x.mode ? (p[B][at] = f(m[B].lastCount + x.length, x.mode) - f(m[B].lastCount, x.mode), m[B].lastCount += x.length) : (m[B] && (m[B].lastCount = x.length), p[B][at] = f(x.length, x.mode) + 4 + t.getCharCountIndicator(x.mode, w));
        }
      }
      E = M;
    }
    for (let A = 0; A < E.length; A++)
      p[E[A]].end = 0;
    return { map: p, table: m };
  }
  function S(_, w) {
    let m;
    const p = t.getBestModeForData(_);
    if (m = t.from(w, p), m !== t.BYTE && m.bit < p.bit)
      throw new Error('"' + _ + '" cannot be encoded with mode ' + t.toString(m) + `.
 Suggested mode is: ` + t.toString(p));
    switch (m === t.KANJI && !c.isKanjiModeEnabled() && (m = t.BYTE), m) {
      case t.NUMERIC:
        return new e(_);
      case t.ALPHANUMERIC:
        return new s(_);
      case t.KANJI:
        return new r(_);
      case t.BYTE:
        return new i(_);
    }
  }
  n.fromArray = function(w) {
    return w.reduce(function(m, p) {
      return typeof p == "string" ? m.push(S(p, null)) : p.data && m.push(S(p.data, p.mode)), m;
    }, []);
  }, n.fromString = function(w, m) {
    const p = u(w, c.isKanjiModeEnabled()), E = g(p), A = y(E, m), C = a.find_path(A.map, "start", "end"), M = [];
    for (let F = 1; F < C.length - 1; F++)
      M.push(A.table[C[F]].node);
    return n.fromArray(h(M));
  }, n.rawSplit = function(w) {
    return n.fromArray(
      u(w, c.isKanjiModeEnabled())
    );
  };
})(Ge);
const Bt = P, Ft = Mt, ji = Ai, Vi = Ci, Ki = Le, Gi = Ue, qt = Oe, Jt = xt, qi = Si, Pt = Fe, Ji = Ve, Wi = q, jt = Ge;
function Yi(n, t) {
  const e = n.size, s = Gi.getPositions(t);
  for (let i = 0; i < s.length; i++) {
    const r = s[i][0], o = s[i][1];
    for (let c = -1; c <= 7; c++)
      if (!(r + c <= -1 || e <= r + c))
        for (let a = -1; a <= 7; a++)
          o + a <= -1 || e <= o + a || (c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 2 && c <= 4 && a >= 2 && a <= 4 ? n.set(r + c, o + a, !0, !0) : n.set(r + c, o + a, !1, !0));
  }
}
function Qi(n) {
  const t = n.size;
  for (let e = 8; e < t - 8; e++) {
    const s = e % 2 === 0;
    n.set(e, 6, s, !0), n.set(6, e, s, !0);
  }
}
function Zi(n, t) {
  const e = Ki.getPositions(t);
  for (let s = 0; s < e.length; s++) {
    const i = e[s][0], r = e[s][1];
    for (let o = -2; o <= 2; o++)
      for (let c = -2; c <= 2; c++)
        o === -2 || o === 2 || c === -2 || c === 2 || o === 0 && c === 0 ? n.set(i + o, r + c, !0, !0) : n.set(i + o, r + c, !1, !0);
  }
}
function Xi(n, t) {
  const e = n.size, s = Pt.getEncodedBits(t);
  let i, r, o;
  for (let c = 0; c < 18; c++)
    i = Math.floor(c / 3), r = c % 3 + e - 8 - 3, o = (s >> c & 1) === 1, n.set(i, r, o, !0), n.set(r, i, o, !0);
}
function Vt(n, t, e) {
  const s = n.size, i = Ji.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (i >> r & 1) === 1, r < 6 ? n.set(r, 8, o, !0) : r < 8 ? n.set(r + 1, 8, o, !0) : n.set(s - 15 + r, 8, o, !0), r < 8 ? n.set(8, s - r - 1, o, !0) : r < 9 ? n.set(8, 15 - r - 1 + 1, o, !0) : n.set(8, 15 - r - 1, o, !0);
  n.set(s - 8, 8, 1, !0);
}
function ts(n, t) {
  const e = n.size;
  let s = -1, i = e - 1, r = 7, o = 0;
  for (let c = e - 1; c > 0; c -= 2)
    for (c === 6 && c--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!n.isReserved(i, c - a)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), n.set(i, c - a, l), r--, r === -1 && (o++, r = 7);
        }
      if (i += s, i < 0 || e <= i) {
        i -= s, s = -s;
        break;
      }
    }
}
function es(n, t, e) {
  const s = new ji();
  e.forEach(function(a) {
    s.put(a.mode.bit, 4), s.put(a.getLength(), Wi.getCharCountIndicator(a.mode, n)), a.write(s);
  });
  const i = Bt.getSymbolTotalCodewords(n), r = Jt.getTotalCodewordsCount(n, t), o = (i - r) * 8;
  for (s.getLengthInBits() + 4 <= o && s.put(0, 4); s.getLengthInBits() % 8 !== 0; )
    s.putBit(0);
  const c = (o - s.getLengthInBits()) / 8;
  for (let a = 0; a < c; a++)
    s.put(a % 2 ? 17 : 236, 8);
  return is(s, n, t);
}
function is(n, t, e) {
  const s = Bt.getSymbolTotalCodewords(t), i = Jt.getTotalCodewordsCount(t, e), r = s - i, o = Jt.getBlocksCount(t, e), c = s % o, a = o - c, l = Math.floor(s / o), d = Math.floor(r / o), u = d + 1, f = l - d, h = new qi(f);
  let g = 0;
  const y = new Array(o), S = new Array(o);
  let _ = 0;
  const w = new Uint8Array(n.buffer);
  for (let C = 0; C < o; C++) {
    const M = C < a ? d : u;
    y[C] = w.slice(g, g + M), S[C] = h.encode(y[C]), g += M, _ = Math.max(_, M);
  }
  const m = new Uint8Array(s);
  let p = 0, E, A;
  for (E = 0; E < _; E++)
    for (A = 0; A < o; A++)
      E < y[A].length && (m[p++] = y[A][E]);
  for (E = 0; E < f; E++)
    for (A = 0; A < o; A++)
      m[p++] = S[A][E];
  return m;
}
function ss(n, t, e, s) {
  let i;
  if (Array.isArray(n))
    i = jt.fromArray(n);
  else if (typeof n == "string") {
    let l = t;
    if (!l) {
      const d = jt.rawSplit(n);
      l = Pt.getBestVersionForData(d, e);
    }
    i = jt.fromString(n, l || 40);
  } else
    throw new Error("Invalid data");
  const r = Pt.getBestVersionForData(i, e);
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
  const o = es(t, e, i), c = Bt.getSymbolSize(t), a = new Vi(c);
  return Yi(a, t), Qi(a), Zi(a, t), Vt(a, e, 0), t >= 7 && Xi(a, t), ts(a, o), isNaN(s) && (s = qt.getBestMask(
    a,
    Vt.bind(null, a, e)
  )), qt.applyMask(s, a), Vt(a, e, s), {
    modules: a,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: s,
    segments: i
  };
}
Be.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let s = Ft.M, i, r;
  return typeof e < "u" && (s = Ft.from(e.errorCorrectionLevel, Ft.M), i = Pt.from(e.version), r = qt.from(e.maskPattern), e.toSJISFunc && Bt.setToSJISFunction(e.toSJISFunc)), ss(t, i, s, r);
};
var Je = {}, se = {};
(function(n) {
  function t(e) {
    if (typeof e == "number" && (e = e.toString()), typeof e != "string")
      throw new Error("Color should be defined as hex string");
    let s = e.slice().replace("#", "").split("");
    if (s.length < 3 || s.length === 5 || s.length > 8)
      throw new Error("Invalid hex color: " + e);
    (s.length === 3 || s.length === 4) && (s = Array.prototype.concat.apply([], s.map(function(r) {
      return [r, r];
    }))), s.length === 6 && s.push("F", "F");
    const i = parseInt(s.join(""), 16);
    return {
      r: i >> 24 & 255,
      g: i >> 16 & 255,
      b: i >> 8 & 255,
      a: i & 255,
      hex: "#" + s.slice(0, 6).join("")
    };
  }
  n.getOptions = function(s) {
    s || (s = {}), s.color || (s.color = {});
    const i = typeof s.margin > "u" || s.margin === null || s.margin < 0 ? 4 : s.margin, r = s.width && s.width >= 21 ? s.width : void 0, o = s.scale || 4;
    return {
      width: r,
      scale: r ? 4 : o,
      margin: i,
      color: {
        dark: t(s.color.dark || "#000000ff"),
        light: t(s.color.light || "#ffffffff")
      },
      type: s.type,
      rendererOpts: s.rendererOpts || {}
    };
  }, n.getScale = function(s, i) {
    return i.width && i.width >= s + i.margin * 2 ? i.width / (s + i.margin * 2) : i.scale;
  }, n.getImageWidth = function(s, i) {
    const r = n.getScale(s, i);
    return Math.floor((s + i.margin * 2) * r);
  }, n.qrToImageData = function(s, i, r) {
    const o = i.modules.size, c = i.modules.data, a = n.getScale(o, r), l = Math.floor((o + r.margin * 2) * a), d = r.margin * a, u = [r.color.light, r.color.dark];
    for (let f = 0; f < l; f++)
      for (let h = 0; h < l; h++) {
        let g = (f * l + h) * 4, y = r.color.light;
        if (f >= d && h >= d && f < l - d && h < l - d) {
          const S = Math.floor((f - d) / a), _ = Math.floor((h - d) / a);
          y = u[c[S * o + _] ? 1 : 0];
        }
        s[g++] = y.r, s[g++] = y.g, s[g++] = y.b, s[g] = y.a;
      }
  };
})(se);
(function(n) {
  const t = se;
  function e(i, r, o) {
    i.clearRect(0, 0, r.width, r.height), r.style || (r.style = {}), r.height = o, r.width = o, r.style.height = o + "px", r.style.width = o + "px";
  }
  function s() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  n.render = function(r, o, c) {
    let a = c, l = o;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), o || (l = s()), a = t.getOptions(a);
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
const ns = se;
function Se(n, t) {
  const e = n.a / 255, s = t + '="' + n.hex + '"';
  return e < 1 ? s + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : s;
}
function Kt(n, t, e) {
  let s = n + t;
  return typeof e < "u" && (s += " " + e), s;
}
function rs(n, t, e) {
  let s = "", i = 0, r = !1, o = 0;
  for (let c = 0; c < n.length; c++) {
    const a = Math.floor(c % t), l = Math.floor(c / t);
    !a && !r && (r = !0), n[c] ? (o++, c > 0 && a > 0 && n[c - 1] || (s += r ? Kt("M", a + e, 0.5 + l + e) : Kt("m", i, 0), i = 0, r = !1), a + 1 < t && n[c + 1] || (s += Kt("h", o), o = 0)) : i++;
  }
  return s;
}
We.render = function(t, e, s) {
  const i = ns.getOptions(e), r = t.modules.size, o = t.modules.data, c = r + i.margin * 2, a = i.color.light.a ? "<path " + Se(i.color.light, "fill") + ' d="M0 0h' + c + "v" + c + 'H0z"/>' : "", l = "<path " + Se(i.color.dark, "stroke") + ' d="' + rs(o, r, i.margin) + '"/>', d = 'viewBox="0 0 ' + c + " " + c + '"', f = '<svg xmlns="http://www.w3.org/2000/svg" ' + (i.width ? 'width="' + i.width + '" height="' + i.width + '" ' : "") + d + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof s == "function" && s(null, f), f;
};
const os = bi, Wt = Be, Ye = Je, as = We;
function ne(n, t, e, s, i) {
  const r = [].slice.call(arguments, 1), o = r.length, c = typeof r[o - 1] == "function";
  if (!c && !os())
    throw new Error("Callback required as last argument");
  if (c) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (i = e, e = t, t = s = void 0) : o === 3 && (t.getContext && typeof i > "u" ? (i = s, s = void 0) : (i = s, s = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = s = void 0) : o === 2 && !t.getContext && (s = e, e = t, t = void 0), new Promise(function(a, l) {
      try {
        const d = Wt.create(e, s);
        a(n(d, t, s));
      } catch (d) {
        l(d);
      }
    });
  }
  try {
    const a = Wt.create(e, s);
    i(null, n(a, t, s));
  } catch (a) {
    i(a);
  }
}
vt.create = Wt.create;
vt.toCanvas = ne.bind(null, Ye.render);
vt.toDataURL = ne.bind(null, Ye.renderToDataURL);
vt.toString = ne.bind(null, function(n, t, e) {
  return as.render(n, e);
});
var cs = Object.defineProperty, N = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && cs(t, e, i), i;
};
const ae = class ae extends T {
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
    const { networks: t, ssids: e } = await R.pollConfig(
      this.hass,
      (s, i) => {
        this._loadingMessage = s, this._isLoading = i;
      }
    );
    this._networks = t, this._ssids = e;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = t.detail.value, s = { ...this._config, ...e };
    this._config.networkId !== e.networkId && (s.ssid = ""), Object.keys(s).forEach((i) => {
      s[i] === "" && delete s[i];
    }), this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: s }, bubbles: !0, composed: !0 }));
  }
  render() {
    if (!this.hass || !this._config) return b``;
    if (this._isLoading)
      return b`
        <div class="editor-container">
          <ha-circular-progress active></ha-circular-progress>
          <div style="margin-top: 16px; color: var(--secondary-text-color);">
            ${this._loadingMessage}
          </div>
        </div>
      `;
    const t = R.getNetworkOptions(this._networks, !0), e = R.getSsidOptions(this._ssids, this._config.networkId, "name"), s = [
      { name: "networkId", selector: { select: { options: t, mode: "dropdown" } } },
      { name: "ssid", selector: { select: { options: e, custom_value: !0, mode: "dropdown" } } },
      { name: "password", selector: { text: {} } },
      { name: "name", selector: { text: {} } }
    ];
    return b`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${s}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
};
ae.styles = H`.editor-container { padding: 16px; }`;
let U = ae;
N([
  z({ attribute: !1 })
], U.prototype, "hass");
N([
  v()
], U.prototype, "_config");
N([
  v()
], U.prototype, "_networks");
N([
  v()
], U.prototype, "_ssids");
N([
  v()
], U.prototype, "_isLoading");
N([
  v()
], U.prototype, "_loadingMessage");
const ce = class ce extends T {
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
    const { ssids: t } = await R.pollConfig(
      this.hass,
      (e, s) => {
        this._loadingMessage = e, this._isLoading = s;
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
    const e = (o = this._config) == null ? void 0 : o.networkId, s = this._ssids.find(
      (c) => c.name === t && (!e || c.networkId === e)
    );
    if (s)
      for (const c in this.hass.states) {
        const a = this.hass.states[c], l = a.attributes;
        if (l.network_id === s.networkId && l.ssid_number === s.number) {
          if (l.psk) return String(l.psk);
          if (l.password) return String(l.password);
          if (a.state && !["unknown", "unavailable"].includes(a.state) && (c.includes("password") || c.includes("psk")))
            return a.state;
        }
      }
    const i = t.toLowerCase().replace(/[^a-z0-9]/g, "_");
    for (const c in this.hass.states)
      if (c.includes(i) && (c.includes("password") || c.includes("psk"))) {
        const a = this.hass.states[c];
        if (a.state && !["unknown", "unavailable"].includes(a.state))
          return a.state;
      }
    return "";
  }
  _generateWifiString(t, e) {
    const s = t.replace(/([\\;,":])/g, "\\$1"), i = e ? e.replace(/([\\;,":])/g, "\\$1") : "";
    return i ? `WIFI:T:WPA;S:${s};P:${i};;` : `WIFI:T:nopass;S:${s};P:;;`;
  }
  async _generateQR() {
    if (!this._config) return;
    const t = this._getValue(this._config.ssid), e = this._getPasswordForSsid(t);
    if (!t) {
      this._qrSvg = "";
      return;
    }
    try {
      const s = this._generateWifiString(t, e);
      this._qrSvg = await vt.toString(s, {
        type: "svg",
        margin: 2,
        color: { dark: "#000000", light: "#ffffff" }
      });
    } catch (s) {
      console.error("Failed to generate QR code", s), this._qrSvg = "";
    }
  }
  render() {
    var s;
    if (!this._config || !this.hass) return b``;
    if (this._isLoading)
      return Nt(
        ((s = this._config) == null ? void 0 : s.name) || "Wi-Fi Access",
        this._loadingMessage,
        "2.3.0-beta.3504"
      );
    const t = this._getValue(this._config.ssid), e = this._getPasswordForSsid(t);
    return b`
      <ha-card .header=${this._config.name || "Wi-Fi Access"}>
        <div class="card-content">
          <div class="ssid-display">${t}</div>
          <div class="qr-container" .innerHTML=${this._qrSvg}></div>
          ${e ? b`<div class="password-display">Password: <code>${e}</code></div>` : ""}
        </div>
        <div class="version">v${"2.3.0-beta.3504"}</div>
      </ha-card>
    `;
  }
};
ce.styles = [
  It,
  H`
      :host { display: block; }
      .card-content { display: flex; flex-direction: column; align-items: center; padding: 16px; gap: 16px; }
      .ssid-display { font-size: 1.5em; font-weight: bold; color: var(--primary-text-color); text-align: center; }
      .qr-container { width: 200px; height: 200px; background: white; padding: 8px; border-radius: 8px; }
      .qr-container svg { width: 100%; height: 100%; }
      .password-display { color: var(--secondary-text-color); text-align: center; }
      code { background: var(--secondary-background-color); padding: 2px 4px; border-radius: 4px; font-family: monospace; }
    `
];
let O = ce;
N([
  z({ attribute: !1 })
], O.prototype, "hass");
N([
  v()
], O.prototype, "_config");
N([
  v()
], O.prototype, "_qrSvg");
N([
  v()
], O.prototype, "_isLoading");
N([
  v()
], O.prototype, "_loadingMessage");
N([
  v()
], O.prototype, "_ssids");
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", O);
customElements.get("meraki-wifi-qr-card-editor") || customElements.define("meraki-wifi-qr-card-editor", U);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-wifi-qr-card") || window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var ls = Object.defineProperty, ot = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && ls(t, e, i), i;
};
const le = class le extends T {
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
    this.hass && await R.pollConfig(
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
        const s = new CustomEvent("navigate", {
          detail: { path: e.navigation_path },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(s);
      } else {
        const s = new CustomEvent("hass-more-info", {
          detail: { entityId: t },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(s);
      }
  }
  _renderStatusDot(t, e, s) {
    const i = !!t && !!this.hass.states[t];
    if (!t || !this.hass.states[t])
      return b`
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
    return o === "ok" || o === "online" || o === "connected" ? c = "var(--success-color)" : o === "warning" ? c = "var(--warning-color)" : (o === "error" || o === "offline" || o === "failed") && (c = "var(--error-color)"), b`
      <div
        class="status-item ${i ? "clickable" : ""}"
        @click="${() => i ? this._handleEntityClick(t, s) : null}"
        role="${i ? "button" : "presentation"}"
        tabindex="${i ? "0" : "-1"}"
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
    var i, r;
    if (!this._config || !this.hass)
      return b``;
    if (this._isLoading)
      return Nt(
        ((i = this._config) == null ? void 0 : i.name) || "Meraki Network Vitals",
        this._loadingMessage,
        "2.3.0-beta.3504"
      );
    const t = this._config.throughput_entity;
    t && this.hass.states[t] && console.log(
      "MERAKI CARD DIAGNOSTIC - Throughput Raw Entity State:",
      this.hass.states[t]
    );
    const e = t ? this.hass.states[t] : void 0, s = e ? (e.state || "0") + " " + (((r = e.attributes) == null ? void 0 : r.unit_of_measurement) || "") : "N/A";
    return b`
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
              <span class="throughput-value">${s}</span>
            </div>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3504"}</div>
      </ha-card>
    `;
  }
};
le.styles = [
  It,
  H`
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
    `
];
let Z = le;
ot([
  z({ attribute: !1 })
], Z.prototype, "hass");
ot([
  v()
], Z.prototype, "_config");
ot([
  v()
], Z.prototype, "_isLoading");
ot([
  v()
], Z.prototype, "_loadingMessage");
const de = class de extends T {
  setConfig(t) {
    this._config = t;
  }
  render() {
    var t, e, s;
    return !this.hass || !this._config ? b`` : b`
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
          .value=${((s = this._config.ap_tap_action) == null ? void 0 : s.action) || "more-info"}
          .configValue=${"ap_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }
  _valueChanged(t) {
    var o;
    if (!this._config) return;
    const e = t.target, s = e.configValue;
    let i = ((o = t.detail) == null ? void 0 : o.value) ?? e.value;
    s && s.endsWith("_tap_action") && (i.startsWith("/") ? i = { action: "navigate", navigation_path: i } : i = { action: i });
    const r = { ...this._config, [s]: i };
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: r },
        bubbles: !0,
        composed: !0
      })
    );
  }
};
de.styles = H`
    ha-textfield,
    ha-entity-picker {
      display: block;
      margin-bottom: 16px;
      width: 100%;
    }
  `;
let _t = de;
ot([
  z({ attribute: !1 })
], _t.prototype, "hass");
ot([
  v()
], _t.prototype, "_config");
customElements.get("meraki-network-vitals-card") || customElements.define("meraki-network-vitals-card", Z);
customElements.get("meraki-network-vitals-card-editor") || customElements.define(
  "meraki-network-vitals-card-editor",
  _t
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
var ds = Object.defineProperty, Qe = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && ds(t, e, i), i;
};
const he = class he extends T {
  constructor() {
    super(...arguments), this._computeLabel = (t) => t.name === "name" ? "Title (Optional)" : t.name === "config_entry_id" ? "Config Entry ID (Optional override)" : t.name;
  }
  setConfig(t) {
    this._config = t;
  }
  render() {
    if (!this.hass || !this._config) return b``;
    const t = [
      { name: "name", selector: { text: {} } },
      { name: "config_entry_id", selector: { text: {} } }
    ];
    return b`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${t}
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
he.styles = H`
    .editor-container { padding: 16px; }
  `;
let yt = he;
Qe([
  z({ attribute: !1 })
], yt.prototype, "hass");
Qe([
  v()
], yt.prototype, "_config");
customElements.get("meraki-guest-access-card-editor") || customElements.define("meraki-guest-access-card-editor", yt);
var hs = Object.defineProperty, I = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && hs(t, e, i), i;
};
const ue = class ue extends T {
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
    const { networks: t, ssids: e, groupPolicies: s, entryId: i } = await R.pollConfig(this.hass, (d, u) => {
      this._loadingMessage = d, this._isLoading = u;
    });
    if (t.length === 0) {
      this._isLoading = !1;
      return;
    }
    this._networks = t, this._ssids = e, this._policies = s, this._configEntryId = ((l = this._config) == null ? void 0 : l.config_entry_id) || i;
    let r = this._formData.network, o = this._formData.ssid, c = this._formData.passphrase, a = this._formData.policy;
    if (t.length > 0 && !r && (r = t[0].id), r && !o) {
      const d = e.filter((u) => u.networkId === r);
      d.length > 0 && (o = String(d[0].number));
    }
    if (r && o && !c && (c = this._getPasswordForSelectedSsid(r, o)), r && !a) {
      const d = this._policies.filter(
        (u) => u.networkId === r
      );
      d.length > 0 && (a = String(
        d[0].groupPolicyId || d[0].id
      ));
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
    const s = parseInt(e, 10);
    let i = "";
    const r = this._ssids.find(
      (o) => o.networkId === t && o.number === s
    );
    r && (i = r.name);
    for (const o in this.hass.states) {
      const a = this.hass.states[o].attributes;
      if (a.network_id === t && a.ssid_number === s) {
        if (i || (i = a.ssid_name || a.ssid || ""), a.psk) return String(a.psk);
        if (a.password) return String(a.password);
      }
    }
    if (i) {
      const o = i.toLowerCase().replace(/[^a-z0-9]/g, "_");
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
    const e = t.detail.value, s = this._formData.network, i = this._formData.ssid;
    let r = { ...this._formData, ...e };
    if (r.network !== s) {
      r.ssid = "", r.passphrase = "", r.policy = "";
      const o = this._ssids.filter(
        (a) => a.networkId === r.network
      );
      o.length > 0 && (r.ssid = String(o[0].number));
      const c = this._policies.filter(
        (a) => a.networkId === r.network
      );
      c.length > 0 && (r.policy = String(
        c[0].groupPolicyId || c[0].id
      ));
    }
    r.ssid && r.ssid !== i && (r.passphrase = this._getPasswordForSelectedSsid(
      r.network,
      r.ssid
    )), this._formData = r;
  }
  render() {
    var o, c;
    if (console.debug("Meraki Guest Access Card Render State:", {
      isLoading: this._isLoading,
      networks: this._networks.length,
      ssids: this._ssids.length,
      policies: this._policies.length,
      formData: this._formData
    }), this._isLoading)
      return Nt(
        ((o = this._config) == null ? void 0 : o.name) || "Meraki Guest Access",
        this._loadingMessage,
        "2.3.0-beta.3504"
      );
    if (this._networks.length === 0)
      return xe(
        "No Wireless Networks",
        "No Meraki wireless networks found. Ensure the integration is configured.",
        "2.3.0-beta.3504"
      );
    const t = R.getNetworkOptions(
      this._networks
    ), e = R.getSsidOptions(
      this._ssids,
      this._formData.network,
      "number"
    ), s = this._policies.filter((a) => a.networkId === this._formData.network).map((a) => ({
      value: String(a.groupPolicyId || a.id),
      label: a.name
    })), i = [
      {
        name: "network",
        selector: { select: { options: t, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: e, mode: "dropdown" } }
      },
      // Only show the policy dropdown if policies successfully loaded for this network
      ...s.length > 0 ? [
        {
          name: "policy",
          selector: {
            select: { options: s, mode: "dropdown" }
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
    return b`
      <ha-card .header="${((c = this._config) == null ? void 0 : c.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? b`<ha-alert
                alert-type="error"
                dismissable
                @alert-dismissed-clicked="${() => this._error = null}"
                >${this._error}</ha-alert
              >` : ""}
          ${this._success ? b`<ha-alert
                alert-type="success"
                dismissable
                @alert-dismissed-clicked="${() => this._success = null}"
                >${this._success}</ha-alert
              >` : ""}

          <div class="form-container">
            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${i}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button
              raised
              .disabled=${this._creating || !r}
              @click=${this._generateAccessKey}
            >
              ${this._creating ? b`<ha-circular-progress
                    active
                    size="small"
                  ></ha-circular-progress>` : "Generate Access Key"}
            </ha-button>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3504"}</div>
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
ue.styles = [
  It,
  H`
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
let k = ue;
I([
  z({ attribute: !1 })
], k.prototype, "hass");
I([
  v()
], k.prototype, "_config");
I([
  v()
], k.prototype, "_formData");
I([
  v()
], k.prototype, "_networks");
I([
  v()
], k.prototype, "_ssids");
I([
  v()
], k.prototype, "_policies");
I([
  v()
], k.prototype, "_creating");
I([
  v()
], k.prototype, "_error");
I([
  v()
], k.prototype, "_success");
I([
  v()
], k.prototype, "_isLoading");
I([
  v()
], k.prototype, "_loadingMessage");
I([
  v()
], k.prototype, "_configEntryId");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", k);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-guest-access-card"
) || window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Manage temporary guest WiFi access. Version: 2.3.0-beta.3504",
  preview: !0,
  version: "2.3.0-beta.3504"
});
export {
  k as MerakiGuestAccessCard
};
