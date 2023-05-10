export function selectTerms(clusters) {
    const terms = createTermsObject(clusters);
    console.log(terms)
    
    const duplicateTerms = getDuplicateTerms(terms);
    const deduplicatedTerms = removeTerms(terms, duplicateTerms);

    console.log(deduplicatedTerms)

    return deduplicatedTerms;
  }
  
  function createTermsObject(clusters) {
    let termsObject = {};
    for (const item of clusters) {
      termsObject[item.cluster] = item.text;
    }
    return termsObject;
  }
  
  function getDuplicateTerms(terms) {
    let termCount = {};
    for (const cluster of Object.values(terms)) {
      for (const term of cluster) {
        const termLower = term.toLowerCase();
        if (!(termLower in termCount)) {
          termCount[termLower] = 0;
        }
        termCount[termLower] += 1;
      }
    }
    return Object.entries(termCount)
                 .filter(([ key, value ]) => value > 1)
                 .map(([ key, value ]) => key);
  }
  
  function removeTerms(clusters, duplicateTerms) {
    let deduplicatedClusters = {};
    for (const [ cluster, terms ] of Object.entries(clusters)) {
      deduplicatedClusters[cluster] = terms.filter((term) => !duplicateTerms.includes(term));
    }
    return deduplicatedClusters;
  }