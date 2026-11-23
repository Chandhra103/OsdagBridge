import test from 'node:test';
import assert from 'node:assert/strict';
import { geometryPayload } from './client.js';

test('geometry input serialization stores explicit metre fields only', () => {
  assert.deepEqual(geometryPayload('24.5', ''), { span_m: 24.5 });
  assert.deepEqual(geometryPayload('', '10'), { width_m: 10 });
  assert.deepEqual(geometryPayload('', ''), {});
});

test('geometry input serialization does not fabricate analysis results', () => {
  const input = geometryPayload('18', '9.5');
  assert.deepEqual(input, { span_m: 18, width_m: 9.5 });
  assert.equal('analysis_results' in input, false);
});
