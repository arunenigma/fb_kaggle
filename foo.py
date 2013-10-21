words = ['private', 'string', 'formatSizeBinary(Int64', 'size,', 'Int32', 'decimals', '=', '2)', '{', 'string[]', 'sizes', '=', '{', '"Bytes",', '"KB",', '"MB",', '"GB",', '"TB",', '"PB",', '"EB",', '"ZB",', '"YB"', '};', 'double', 'formattedSize', '=', 'size;', 'Int32', 'sizeIndex', '=', '0;', 'while', '(formattedSize', '>=', '1024', '&', 'sizeIndex', '<', 'sizes.Length)', '{', 'formattedSize', '/=', '1024;', 'sizeIndex', '+=', '1;', '}', 'return', 'string.Format("{0}', '{1}",', 'Math.Round(formattedSize,', 'decimals).ToString(),', 'sizes[sizeIndex]);', '}']
from nltk import trigrams

tri_grams = trigrams(words)
print tri_grams
