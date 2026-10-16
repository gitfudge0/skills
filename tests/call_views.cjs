const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const runtime = require.resolve('../plan/runtime/htmlplan.js');
require(runtime);
const NW = globalThis.HtmlPlan;
const source = '~ **confirmLogout**() @ src/logout.ts:10 -- confirm first\n  english: Confirm logout\n+   DELETE /sign_out @ src/api.ts:20\n    english: Ask the server to sign out\n    legacyStep() @ src/legacy.ts:30';
const parsed = NW.parseCalls(source);
assert.deepEqual(parsed.errors, []);
assert.equal(parsed.nodes.length, 3);
assert.equal(parsed.nodes[0].english, 'Confirm logout');
assert.equal(parsed.nodes[0].name, 'confirmLogout()');
assert.equal(parsed.nodes[1].english, 'Ask the server to sign out');
assert.equal(parsed.nodes[1].parent, parsed.nodes[0]);
assert.equal(parsed.nodes[2].english, '');
assert.equal(parsed.nodes[0].loc, 'src/logout.ts:10');
assert.equal(parsed.nodes[0].note, 'confirm first');
assert.equal(parsed.nodes[0].isNew, true);
assert.ok(NW.parseCalls('english: Orphan translation').errors.length);
assert.ok(NW.parseCalls('~ foo()\n  english: ').errors.some(e => e.includes('needs authored text')));
assert.ok(NW.parseCalls('~ foo()\n  english: First\n  english: Duplicate').errors.length);

// A small DOM surface exercises the actual registered renderer, without dependencies.
class Element {
  constructor(tag, attrs = {}) { this.tag = tag; this.attrs = attrs; this.children = []; this.childNodes = this.children; this.dataset = {}; this.events = {}; this._text = ''; this.classes = new Set((attrs.class || '').split(' ')); this.classList = { add: (...cs) => cs.forEach(c => this.classes.add(c)), contains: c => this.classes.has(c), toggle: (c, on) => on ? this.classes.add(c) : this.classes.delete(c) }; }
  append(...items) { items.flat().filter(x => x != null && x !== '').forEach(x => this.children.push(x)); }
  prepend(...items) { this.children.unshift(...items.filter(Boolean)); }
  set textContent(t) { this._text = String(t); this.children.length = 0; }
  get textContent() { return this._text + this.children.map(x => typeof x === 'string' ? x : x.textContent).join(''); }
  set innerHTML(t) { assert.equal(t, ''); this.children.length = 0; }
  getAttribute(k) { return this.attrs[k] ?? null; }
  setAttribute(k, v) { this.attrs[k] = v; }
  hasAttribute(k) { return k in this.attrs; }
  addEventListener(k, fn) { this.events[k] = fn; }
  querySelectorAll(q) { const cls = q.startsWith('.') && q.slice(1); return this.children.filter(x => x instanceof Element).flatMap(x => [...(cls && x.classes.has(cls) ? [x] : []), ...x.querySelectorAll(q)]); }
  querySelector(q) { return this.querySelectorAll(q)[0] || null; }
}
const h = (tag, attrs, ...children) => { const node = new Element(tag, attrs || {}); node.append(...children); return node; };
const el = new Element('doc-calls', { id: 'logout', title: 'Logout' }); el.id = 'logout';
const S = { strikes: { 'calls:logout:n2': { reason: 'Keep session' } }, comments: { 'calls:logout:n1': { text: 'Check this' } } };
const template = new Element('template', { for: 'confirmLogout' });
template.content = { cloneNode: () => new Element('code', {}) };
const context = { NW, srcOf: () => source, errBox: (_, errors) => assert.deepEqual(errors, []), $$: (q, root) => q === 'doc-calls' ? [el] : q === ':scope > template[for]' ? [template] : root.querySelectorAll(q), h, S, secLabel: () => '', save() {}, openComment() {}, setTimeout, requestAnimationFrame() {}, upgradeWithin() {} };
const code = fs.readFileSync(runtime, 'utf8');
const start = code.indexOf("define('doc-calls', (el) => {");
const end = code.indexOf('\n/* ── doc-tree', start);
context.define = (_, render) => render(el);
vm.runInNewContext(code.slice(start, end), context);
let rows = el.querySelectorAll('.cl-row');
assert.equal(rows.length, 3);
assert.equal(rows[0].querySelector('.cl-nm').textContent, 'Confirm logout');
assert.equal(rows[2].querySelector('.cl-nm').textContent, 'legacyStep()');
assert.equal(rows[0].querySelector('.cl-loc').textContent, 'src/logout.ts:10');
assert.ok(rows[0].classList.contains('has-comment'));
assert.ok(rows[1].classList.contains('struck'));
rows[0].events.click({ target: { closest: () => null } });
rows = el.querySelectorAll('.cl-row');
rows[0].classList.add('sel');
assert.ok(rows[0].classList.contains('open'));
const detail = el.querySelector('.cl-det');
assert.ok(detail);
const buttons = el.querySelectorAll('.cl-view-btn');
assert.deepEqual(buttons.map(b => b.textContent), ['Plain English', 'Technical']);
assert.equal(buttons[0].getAttribute('aria-pressed'), 'true');
buttons[1].attrs.onclick();
assert.equal(rows[0].querySelector('.cl-nm').textContent, 'confirmLogout()');
assert.equal(buttons[1].getAttribute('aria-pressed'), 'true');
buttons[0].attrs.onclick();
assert.equal(rows[0].querySelector('.cl-nm').textContent, 'Confirm logout');
assert.equal(el.querySelectorAll('.cl-row')[0], rows[0]);
assert.equal(el.querySelector('.cl-det'), detail);
assert.ok(rows[0].classList.contains('sel'));
assert.ok(rows[0].classList.contains('open'));
assert.ok(rows[0].classList.contains('has-comment'));
assert.ok(rows[1].classList.contains('struck'));
assert.equal(S.strikes['calls:logout:n2'].reason, 'Keep session');
// Re-rendering after a strike must retain the chosen view and stable feedback keys.
buttons[1].attrs.onclick();
rows[1].querySelector('.cl-acts').children[1].attrs.onclick({ stopPropagation() {} });
assert.equal(el.querySelectorAll('.cl-row')[0].querySelector('.cl-nm').textContent, 'confirmLogout()');
assert.equal(S.strikes['calls:logout:n2'], undefined);
assert.ok(el.querySelectorAll('.cl-row')[0].classList.contains('has-comment'));
el._reset();
assert.equal(el.querySelectorAll('.cl-row')[0].querySelector('.cl-nm').textContent, 'Confirm logout');
assert.equal(el.querySelectorAll('.cl-view-btn')[0].getAttribute('aria-pressed'), 'true');
console.log('PASS: paired parser, legacy fallback, default view, toggle and row/feedback preservation');
