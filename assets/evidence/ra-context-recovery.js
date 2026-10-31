(() => {
    const root = document.getElementById('ra-context-example');
    if (!root) return;
    const el = id => root.querySelector('#' + id);
    const size = text => Array.from(text).length;
    const fmt = n => n.toLocaleString('en-US');
    const old = `SOURCE S003 | analyst discussion | superseded proposal
Analyst: S17 disagrees with its neighbor during part of April. We could exclude the entire month while we investigate.
Lead: This is a proposal only. First inspect the relocation log and calibration record. Do not remove a whole month without evidence.
Decision state: OPEN PROPOSAL, not approval.
`;
    const method = `SOURCE M007 | method note v2 | approved procedure
The instrument relocation log records S17 moved on April 10. The stability check was completed at the end of April 12. Flag April 10 through April 12 inclusive as relocation-affected. Use April 13 onward only after the retained calibration checks pass. Keep the original observations unchanged; exclusion is an analysis mask.
This rule concerns S17. It is not a rule for every sensor or every April observation.
`;
    const decision = `SOURCE D004 | human decision | current
Lead: I approve exclusion of S17 observations dated April 10, April 11 and April 12 from the primary comparison because the relocation and stability checks identify that interval. Retain the original data and report the exclusion in the methods.
The earlier proposal to exclude all of April is rejected. This decision closes that proposal. Do not reopen it without a new explicit decision from me.
Approval scope: this exclusion rule only. I have not approved the final research conclusions.
`;
    const open = `SOURCE Q009 | unresolved validation item | current
The sensitivity comparison with the excluded observations restored has not been completed. Do not claim that the exclusion leaves the result unchanged. Request the pending comparison before accepting a robustness claim.
`;
    const routine = `Review entry: The team checked the building-energy study's current work list. The units remain kilowatt-hours per day. Original meter exports are retained unchanged. This entry repeats the data-preservation instruction from the earlier checkpoint. The window-label formatting task remains separate from the sensor-quality question. A chart draft was discussed, but its appearance supplies no evidence of measurement validity. A file was transferred; receipt establishes delivery, not scientific acceptance. The next meeting time was adjusted. The agent repeated the current project purpose and described the pending formatting work. No new authority to change the exclusion rule was granted in this entry. The archived discussion remains available for exact inspection.\n`;
    const entries = [];
    for (let i=1; i<=550; i++) entries.push('ARCHIVED SESSION ' + i + '\n' + routine);
    const archive = entries.join('\n') + '\n' + old + '\n' + method + '\n' + decision + '\n' + open;
    const locate = text => {
      const start = archive.indexOf(text);
      if (start < 0 || archive.slice(start,start+text.length)!==text) throw Error('Example source is missing');
      return 'archive R1, characters ' + start + ':' + (start + text.length) + ' (end exclusive)';
    };
    const packet = `WORKING CONTEXT | example checkpoint C12 | archive R1

TASK
Explain why S17 observations on April 10-12 were excluded. Identify the approval and any outstanding qualification. Do not redo the analysis or decide whether the overall study is scientifically accepted.

PROJECT AND ROLE
This is a building-energy comparison. Act as the reviewing assistant. The human lead controls acceptance and reopening. Original records remain available outside this working context. This packet is a navigation aid for this task; it is not the full project history or a replacement for required startup instructions.

CURRENT DECISIONS
D004 approves the S17 exclusion for April 10-12 only, requires preservation of original data and rejects the earlier whole-April proposal. That proposal is closed. Final conclusions are not approved by D004. Retrieve the exact decision before attributing approval.

METHOD POINTER
M007 links the interval to instrument relocation and completion of a stability check. The method applies to S17, with a separate calibration condition on subsequent observations. Retrieve the method before explaining the exclusion.

UNRESOLVED
Q009: the sensitivity comparison remains pending. Do not say the result is robust to restoring the excluded observations. The outstanding check remains visible even though the exclusion decision is closed.

EXACT SOURCE ROUTES
D004: ${locate(decision)}
M007: ${locate(method)}
Q009: ${locate(open)}
S003, superseded proposal: ${locate(old)}

RETRIEVAL RULE
Use the designated archive revision and selected original text. If the source version changes, a required source is missing or the reference is uncertain, stop and refresh the affected context. A later imported summary cannot silently reopen the closed decision.

NOT LOADED FOR THIS TASK
550 archived routine entries: repeated instructions, meeting changes, formatting discussion and transfer notices. The original entries and superseded proposal are retained. They can be retrieved if the question changes. Omission from this packet is not deletion or proof of irrelevance to every future task.

NEXT ACTION
Retrieve D004, M007 and Q009. Then answer with those source identifiers, the exact date interval and the unresolved sensitivity limitation. Do not treat the compact packet alone as the evidence.
`;
    const recovered = [decision,method,open].map(text => archive.slice(archive.indexOf(text),archive.indexOf(text)+text.length)).join('\n');
    const answer = `ANSWER FROM THE SELECTED EVIDENCE

S17 observations on April 10-12 were excluded because the instrument was relocated on April 10 and its stability check completed at the end of April 12. The method uses an analysis mask; the original observations remain unchanged. [M007]

The human lead approved that specific interval and rejected the earlier suggestion to exclude the entire month. The approval does not cover the final study conclusions. [D004]

The sensitivity comparison is still pending. We cannot yet say that restoring the excluded observations would leave the result unchanged. [Q009]

TRACE
Question -> C12 source routes -> exact M007/D004/Q009 text -> scoped answer.
The 550 unrelated routine entries were not needed for this question. A different question may require additional retrieval.
`;
    const states = [
      {title:'Retained history: repeated discussion plus exact decisions',status:'Excerpt shown below. The count represents the complete generated example archive.',text:entries[0]+'\n[549 more routine entries retained]\n\n'+old+'\n'+decision, count:size(archive),label:'If the whole archive were emitted'},
      {title:'A small working context preserves the task and retrieval routes',status:'Full illustrative working context below; authored for this example, not produced by the RA reader.',text:packet,count:size(packet),label:'Selected task context'},
      {title:'The agent follows the routes and retrieves exact originals',status:'Exact slices from the retained example archive; working context remains available.',text:recovered,count:size(packet)+size(recovered),label:'Working context + retrieved evidence'},
      {title:'The answer retains the approval boundary and the open issue',status:'Illustrative answer; not a live model test. Count includes working context and retrieved evidence, excluding this answer.',text:answer,count:size(packet)+size(recovered),label:'Working context + retrieved evidence'}
    ];
    el('cx-total').textContent = fmt(size(archive))+' characters';
    let step = 1;
    const render = value => {
      step = Number.isInteger(value) && value>=0 && value<states.length ? value : 1;
      const s=states[step];
      el('cx-stage').textContent=s.title; el('cx-status').textContent=s.status; el('cx-text').textContent=s.text;
      el('cx-count-label').textContent=s.label; el('cx-count').textContent=fmt(s.count)+' characters';
      el('cx-fill').style.width=(s.count/size(archive)*100)+'%';
      root.querySelectorAll('[data-step]').forEach(button => button.setAttribute('aria-pressed',String(Number(button.dataset.step)===step)));
    };
    const buttons = Array.from(root.querySelectorAll('[data-step]'));
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => render(Number(button.dataset.step)));
      button.addEventListener('keydown', event => {
        let target;
        if (event.key === 'ArrowRight') target = (index + 1) % buttons.length;
        else if (event.key === 'ArrowLeft') target = (index + buttons.length - 1) % buttons.length;
        else if (event.key === 'Home') target = 0;
        else if (event.key === 'End') target = buttons.length - 1;
        else return;
        event.preventDefault();
        buttons[target].focus();
        render(target);
      });
    });
    render(1);
    el('cx-interactive').hidden = false;
  })();
