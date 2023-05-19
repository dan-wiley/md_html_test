function removePTagsInLiBlocksRecursive(element)
  if element.tag == "BulletList" or element.tag == "OrderedList" then
    element.content = pandoc.walk_block(element.content, {
      Para = function(para)
        return pandoc.Span(para.content)
      end
    })
  end
  return element
end

return {
  { Block = removePTagsInLiBlocksRecursive }
}
